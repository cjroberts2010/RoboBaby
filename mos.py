import utime

class mos:
    def __init__(self,pin, interval):
        self.pin = pin
        self.interval = interval
        
    def pulse(self):
        self.pin.high()
        utime.sleep_ms(self.interval)
        self.pin.low()
        

if __name__ == "__main__":
    import pyb
    MPin = pyb.Pin(pyb.Pin.board.PB8, mode = pyb.Pin.OUT_PP)
    moss = mos(MPin, 1000)
    while True:
        moss.pulse()
        utime.sleep_ms(1000)