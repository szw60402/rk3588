import argparse
import signal
import sys
from pathlib import Path

import cv2
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from camera import Camera
from detector import Detector
from gpio_io import GPIOOutput
from modbus_io import ModbusIO
from rtsp_stream import RTSPStream


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def draw(frame, detections, class_names):
    for d in detections:
        label = class_names[d.cls_id] if d.cls_id < len(class_names) else str(d.cls_id)
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
        cv2.putText(frame, f"{label} {d.score:.2f}", (d.x1, max(16, d.y1 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)

    cam_cfg = cfg["camera"]
    camera = Camera(cam_cfg["index"], cam_cfg["width"], cam_cfg["height"])

    det_cfg = cfg["detector"]
    class_names = det_cfg.get("class_names") or []
    detector = Detector(det_cfg["model_path"], det_cfg["conf_threshold"],
                        det_cfg["nms_threshold"], class_names)
    detector_ready = True
    try:
        detector.load()
    except Exception as exc:
        detector_ready = False
        print(f"[warn] detector not loaded: {exc}")
        print("[warn] capture and stream only")

    modbus = None
    if cfg["modbus"]["enabled"]:
        m = cfg["modbus"]
        modbus = ModbusIO(m["host"], m["port"], m["unit_id"], m["register"])
        modbus.connect()

    gpio = None
    if cfg["gpio"]["enabled"]:
        g = cfg["gpio"]
        gpio = GPIOOutput(g["chip"], g["line"], g["pulse_ms"])

    stream = None
    if cfg["rtsp"]["enabled"]:
        r = cfg["rtsp"]
        stream = RTSPStream(r["url"], r["width"], r["height"], r["fps"])

    stop = False

    def on_signal(signum, frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    try:
        while not stop:
            frame = camera.read()
            if frame is None:
                print("[warn] empty frame, stop")
                break

            detections = detector.detect(frame) if detector_ready else []
            if detections:
                if modbus is not None:
                    modbus.write_count(len(detections))
                if gpio is not None:
                    gpio.pulse()

            if stream is not None:
                stream.write(draw(frame, detections, class_names))
            else:
                cv2.imshow("rk3588 inspection", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
    finally:
        camera.release()
        detector.close()
        if modbus is not None:
            modbus.close()
        if gpio is not None:
            gpio.close()
        if stream is not None:
            stream.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()