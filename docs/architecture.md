# rk3588 视觉质检工位 — 架构

## 数据流

1. `camera.py` 从 USB/MIPI 相机取帧（OpenCV）。
2. `detector.py` 负责 RKNN 推理：预处理、推理、解码、NMS。
3. `main.py` 根据检测结果判定 OK/NG：
   - NG 时调 `modbus_io.write_count()` 写寄存器，或调 `gpio_io.pulse()` 打一个脉冲。
4. 画框后交给 `rtsp_stream.py`，由 ffmpeg 推 RTSP；没有开 RTSP 时本地窗口预览。

## 模块接口

- `Camera.read() -> frame | None`
- `Detector.load()` / `Detector.detect(frame) -> list[Detection]`
- `ModbusIO.write_count(count)`
- `GPIOOutput.pulse()`
- `RTSPStream.write(frame)`

## 待定

- 相机型号和安装距离
- 缺陷类别、判定阈值、节拍
- 模型输入尺寸、量化方式、是否多模型
- 下位机是 Modbus TCP/RTU 还是 GPIO
- 是否需要光电触发、剔除机构
- 现场光照和遮光方案