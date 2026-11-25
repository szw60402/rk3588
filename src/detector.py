from dataclasses import dataclass
from pathlib import Path


@dataclass
class Detection:
    cls_id: int
    score: float
    x1: int
    y1: int
    x2: int
    y2: int


class Detector:
    """RKNN 推理接口。模型转换、前后处理方案待定，先固定调用方式。"""

    def __init__(self, model_path, conf=0.45, nms=0.45, class_names=None):
        self.model_path = Path(model_path)
        self.conf = conf
        self.nms = nms
        self.class_names = class_names or []
        self._rknn = None
        self._ready = False

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"model not found: {self.model_path}")
        from rknnlite.api import RKNNLite

        rknn = RKNNLite()
        if rknn.load_rknn(str(self.model_path)) != 0:
            raise RuntimeError("load_rknn failed")
        if rknn.init_runtime() != 0:
            raise RuntimeError("init_runtime failed")
        self._rknn = rknn
        self._ready = True

    def detect(self, frame):
        if not self._ready:
            return []
        # TODO: letterbox、归一化、推理、解码、NMS
        raise NotImplementedError("RKNN postprocess not implemented")

    def close(self):
        if self._rknn is not None:
            self._rknn.release()
            self._rknn = None