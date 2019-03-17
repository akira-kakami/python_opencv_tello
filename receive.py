import socket
import time

TELLO_IP = '192.168.10.1'
TELLO_CMD_PORT = 8889
TELLO_STAT_PORT= 8890

LOCAL_IP = ''
LOCAL_IP_CMD = 9000



sock_rec = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock_rec.bind( ( LOCAL_IP, TELLO_STAT_PORT ) )
sock_rec.setblocking(1)
sock_rec.settimeout(5)
sock_rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_cmd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock_cmd.bind( ( LOCAL_IP, LOCAL_IP_CMD) )
sock_cmd.sendto( 'command'.encode( encoding='utf-8' ), (TELLO_IP, TELLO_CMD_PORT) )

while True:
    k = input()
    if k == 'q':
        break
    try:
        data,server = sock_rec.recvfrom(1518)
    except socket.error as e:
        print('Socket error' + str(e) )
        pass
    else:
        print(data)
