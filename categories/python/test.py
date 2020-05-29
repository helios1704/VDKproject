import serial

ser = serial.Serial('COM16', baudrate = 1000000, timeout=1)
file2 = open(r"python\data.txt","w")
i = 0
while (1)   :
    i=i+1
    arduinoData = ser.readline().decode('utf-8')
    file2.write(arduinoData)
    if (i>=290) :
        break
serial.Serial('COM16', baudrate = 1000000).close()