# rk3588 — 视觉质检工位（骨架）

RK3588 + 相机 + NPU 的缺陷检测工位。现在只是框架：接口和目录先定下来，模型、相机型号、下位机方案都还没定。

## 链路

```
相机采集 → 预处理 → RKNN YOLO 推理 → 缺陷判定
                                      ├─ Modbus 写结果 / GPIO 脉冲
                                      └─ 画框 → RTSP 推流
```

## 目录

```
rk3588/
├── config/config.yaml      # 相机、模型、Modbus、GPIO、RTSP 参数
├── src/
│   ├── main.py             # 主循环
│   ├── camera.py           # 相机采集
│   ├── detector.py         # RKNN 推理接口（后处理待填）
│   ├── modbus_io.py        # Modbus TCP 写结果
│   ├── gpio_io.py          # GPIO 脉冲（待接 libgpiod）
│   └── rtsp_stream.py      # ffmpeg 推 RTSP
├── docs/architecture.md    # 接口和待定项
├── models/                 # .rknn 模型放这里（不提交）
└── requirements.txt
```

## 当前状态

- [x] 目录、配置、模块接口
- [x] 相机采集、RTSP 推流骨架
- [ ] RKNN 模型转换与推理后处理
- [ ] Modbus / GPIO 与下位机实际联调
- [ ] 数据集、标注、训练

没有模型或没装 RKNN 时，程序会跳过推理，只跑采集和推流。

## 运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 src/main.py --config config/config.yaml
```

按 Esc 退出。

## 待定

- 相机：USB 还是 MIPI CSI，分辨率与帧率
- 检测目标：缺陷类型、判定阈值、节拍要求
- 下位机：Modbus RTU/TCP 还是 GPIO 直接触发
- 模型：YOLOv8n / YOLOv5s，输入尺寸与量化方式
- 光照：是否需要补光/遮光罩