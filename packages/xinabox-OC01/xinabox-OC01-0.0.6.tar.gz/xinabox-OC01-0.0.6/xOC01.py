from xCore import xCore

PCA9536_REG_INPUT_PORT = 0x00
PCA9536_REG_OUTPUT_PORT = 0x01
PCA9536_REG_POL_INVERSION = 0x02
PCA9536_REG_CONFIG = 0x03

PCA9536_CONF_OUTPUT = 0x00
PCA9536_CONF_INPUT = 0x0F

PCA9536_ALL_OUTPUTS_OFF = 0x00

PCA9536_PIN0_OUTPUT = 0x00
PCA9536_PIN0_INPUT = 0x01

PCA9536_PIN1_OUTPUT = 0x00
PCA9536_PIN1_INPUT = 0x02

PCA9536_PIN2_OUTPUT = 0x00
PCA9536_PIN2_INPUT = 0x04

PCA9536_PIN3_OUTPUT = 0x00
PCA9536_PIN3_INTPUT = 0x08

class xOC01:

    OUT0 = 0x01
    OUT1 = 0x02
    OUT2 = 0x04
    OUT3 = 0x08

    def __init__(self, addr=0x41):
        self.i2c = xCore()
        self.addr = addr
        self.begin()

    def init(self, pins):
        self.i2c.write_bytes(self.addr, PCA9536_REG_OUTPUT_PORT, pins)
        self.i2c.write_bytes(self.addr, PCA9536_REG_CONFIG, PCA9536_CONF_OUTPUT)

    def begin(self):
        self.init(PCA9536_ALL_OUTPUTS_OFF)

    def digitalWrite(self, pin, state):
        pin_state = self.i2c.write_read(self.addr, PCA9536_REG_OUTPUT_PORT, 1)[0]
        if state == True:
            pin_state |= (pin_state | pin)
            self.i2c.write_bytes(self.addr, PCA9536_REG_OUTPUT_PORT, pin_state)
        elif state == False:
            pin_state &= ~(1 << pin_state | pin)
            self.i2c.write_bytes(self.addr, PCA9536_REG_OUTPUT_PORT, pin_state)

    def getStatus(self):
        pin_state = self.i2c.write_read(self.addr, PCA9536_REG_OUTPUT_PORT, 1)[0]
        return pin_state
