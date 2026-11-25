import subprocess


class RTSPStream:
    """把 BGR 帧通过 ffmpeg 推到 RTSP。需要板端已装 ffmpeg 和 RTSP 服务。"""

    def __init__(self, url, width, height, fps=15):
        self.proc = subprocess.Popen(
            [
                "ffmpeg", "-loglevel", "error",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
                "-f", "rtsp", url,
            ],
            stdin=subprocess.PIPE,
        )

    def write(self, frame):
        if self.proc.stdin is None:
            return
        try:
            self.proc.stdin.write(frame.tobytes())
        except BrokenPipeError:
            print("[rtsp] ffmpeg pipe closed")

    def close(self):
        if self.proc.stdin is not None:
            self.proc.stdin.close()
        self.proc.wait(timeout=3)