from pymodbus.client import ModbusTcpClient


class ModbusIO:
    def __init__(self, host, port=502, unit_id=1, register=0):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.register = register
        self.client = None

    def connect(self):
        self.client = ModbusTcpClient(self.host, port=self.port)
        if not self.client.connect():
            raise RuntimeError(f"modbus connect failed: {self.host}:{self.port}")

    def write_count(self, count):
        if self.client is None:
            return
        self.client.write_register(self.register, int(count), slave=self.unit_id)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None