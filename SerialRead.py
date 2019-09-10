import serial
from serial.serialutil import SerialException
import matplotlib.pyplot as plt

recording = True
connected = False

Y = [0] * 2000
X = list(range(0,2000))

plt.ion()
graph = plt.plot(X,Y)[0]
plt.ylim(0, 300)

print('Input port number')
pn = 'COM' + input()

try:
    bteLink = serial.Serial(pn, timeout = 2)  # open serial port
except SerialException:
    print('Could not open port')
    exit()
connected = True
print('Opened port:', end =" ")
print(bteLink.name)         # check which port was really used
bteLink.reset_input_buffer() #clear the input buffer
print('input file name')
fileName = input()
print('press Ctrl + C to stop recording')
with open(fileName, mode='wb') as data_file:
    while recording:
        if connected:
            try:
                
                bytedata = bteLink.read_until()
                strdata = bytedata.decode("utf-8")
                comma2 = strdata.find(',',7)
                comma3 = strdata.find(',',comma2 +1)
                
                try:
                    load = float(strdata[comma2+1:comma3])
                
                    Y.append(load)
                    Y.pop(0)
                    
                    graph.set_ydata(Y)
                    plt.draw()
                    plt.pause(0.01)
                    
                    data_file.write(bytedata)
                    print(strdata)
                    
                except ValueError:
                    print("Lost Connection")
                    connected = False
            except KeyboardInterrupt:
                print('Finished Recording')  
                data_file.close()   
                recording = False 
        else:
            bteLink.close()
            try:
                bteLink = serial.Serial('COM8', timeout = 2)  # open serial port
                print("reconnected")
                connected = True;
            except SerialException:
                print('Could not re-open port')
bteLink.close()

