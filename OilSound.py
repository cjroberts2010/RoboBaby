import pyb
if __name__ == '__main__':
    PinA0 = pyb.ADC(pyb.Pin.board.PA0)
    counter = 0
    val = []
    while counter < 1023:
        print(PinA0.read())
        
        counter+=1
    
