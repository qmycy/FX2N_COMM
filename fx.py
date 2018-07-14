import serial
import threading
ser=serial.Serial('com6',baudrate=9600,bytesize=serial.SEVENBITS,parity=serial.PARITY_EVEN,stopbits=1,timeout=0.5)

#ser.open()


def gen_device_read_cmd(start,nbyte):
    
    device_read_cmd=[]

    device_read_cmd.append(b'\x02')
    device_read_cmd.append(b'0')
    for i in format(start,'04X').encode():
        device_read_cmd.append(chr(i).encode())
    for i in format(nbyte,'02X').encode():
        device_read_cmd.append(chr(i).encode())
    device_read_cmd.append(b'\x03')

    check=0
    for i in device_read_cmd[1:]:
        check+=ord(i)

    for i in format(check%256,'02X').encode():
        device_read_cmd.append(chr(i).encode())

    return device_read_cmd

def gen_device_write_cmd(start,nbyte,data):
    
    device_write_cmd=[]

    device_write_cmd.append(b'\x02')
    device_write_cmd.append(b'1')
    for i in format(start,'04X').encode():
        device_write_cmd.append(chr(i).encode())
    for i in format(nbyte,'02X').encode():
        device_write_cmd.append(chr(i).encode())
    for i in format(data,'02X').encode():
        device_write_cmd.append(chr(i).encode())

    device_write_cmd.append(b'\x03')

    check=0
    for i in device_write_cmd[1:]:
        check+=ord(i)

    for i in format(check%256,'02X').encode():
        device_write_cmd.append(chr(i).encode())

    return device_write_cmd

def gen_force_on_cmd(start,data):
    
    device_write_cmd=[]

    device_write_cmd.append(b'\x02')
    if (data) :
        device_write_cmd.append(b'7')
    else:
        device_write_cmd.append(b'8')
    start_l=start%256;
    start_h=start>>8;
    for i in format(start_l,'02X').encode():
        device_write_cmd.append(chr(i).encode())
    for i in format(start_h,'02X').encode():
        device_write_cmd.append(chr(i).encode())
    device_write_cmd.append(b'\x03')

    check=0
    for i in device_write_cmd[1:]:
        check+=ord(i)

    for i in format(check%256,'02X').encode():
        device_write_cmd.append(chr(i).encode())

    return device_write_cmd


request= gen_device_read_cmd(0x8000,32)

for i in request:
    ser.write(i)

answer=ser.read(256)
for i in answer:
    print(chr(i))
