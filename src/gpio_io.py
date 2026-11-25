import time


class GPIOOutput:
    """GPIO 脉冲输出。板子的 gpiochip 编号确认后再接 libgpiod，现在只打印。"""

    def __init__(self, chip="gpiochip4", line=12, pulse_ms=100):
        self.chip = chip
        self.line = line
        self.pulse_ms = pulse_ms

    def pulse(self):
        print(f"[gpio] {self.chip}:{self.line} -> 1, {self.pulse_ms}ms")
        time.sleep(self.pulse_ms / 1000.0)
        print(f"[gpio] {self.chip}:{self.line} -> 0")

    def close(self):
        pass