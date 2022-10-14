"""
@file PIR.py

@brief This file contains a class and tester for the PIR motion sensor.
@detail This file contains the class PIR, which will have one task: reading the value from the digital input pin
        that is connected to the PIR sensor kit. The PIR will return a single boolean that can be used in conjunction
        with the other input devices to activate the device.
        
@author Christian Roberts
"""

import pyb

class PIR:
    def __init__ (self, pin_in):
        """
        @brief Initializes the PIR reader
        @param pyb.Pin object that connects to the PIR reader.
        """
        self.pin_in = pin_in
        self.pinpir = pyb.Pin(self.pin_in, mode = pyb.Pin.IN)
        
    def read (self):
        while True:
            val = self.pinpir.value()
            yield (val)
            
if __name__ == '__main__':
    PIR1 = PIR(pyb.Pin.board.PA9)
    import utime
    counter = 0
    while counter < 1000:
        counter += 1
        val = PIR1.read()
        if counter%10 == 0:
            print(next(val))
        else:
            pass
        utime.sleep_ms(10)
        