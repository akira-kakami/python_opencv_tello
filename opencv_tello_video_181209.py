import cv2
import time
import socket
import threading
import queue

TELLO_IP = '192.168.10.1'
TELLO_CMD_PORT = 8889
TELLO_STAT_PORT = 8890
TELLO_VIDEO_PORT = 11111
LOCAL_IP = '0.0.0.0'
LOCAL_PORT = 18010


recv_cmd_enable = True
receive_stat_enable = True
def prep_cmd_socket():
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.settimeout( 1 )
    sock.bind( ( LOCAL_IP, LOCAL_PORT ) )
    return sock

def prep_stat_socket():
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind( ( LOCAL_IP, TELLO_STAT_PORT ) )
    sock.settimeout( 1 )
    sock.setblocking( 1 )
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock


def send_cmd( command, sock ):
    sock.sendto( command, (TELLO_IP, TELLO_CMD_PORT) )


def recv_cmd( queue, sock ):
    while recv_cmd_enable == True:
        try:
            rcvdata, server = sock.recvfrom(1518)
            queue.put( rcvdata.decode( encoding='utf-8' ) )
        except:
            continue
    print('Recv_cmd terminated')


def receive_stat( queue, sock ):
    while receive_stat_enable == True:
        try:
            data, server = sock.recvfrom(1518)
        except:
            continue
        else:
            queue.put( data.decode( encoding = 'utf-8' ) )

    print('receive_stat terminated')

video_display_thread_enabled = True

#video_display_threadで実行する関数．
#モニタ上に，フライトデータとインカムの映像を表示する．
#フライトデータとスレッドの管理変数は，グローバル変数になっている．
def video_display( cap ):
    while video_display_thread_enabled:
        ret, frame = cap.read()
        if ret:
            #if 'pitch' in flight_data_dict:
            #    pitch = flight_data_dict['pitch']
            #    roll = flight_data_dict['roll']
            #    yaw = flight_data_dict['yaw']
            #    vgx = flight_data_dict['vgx']
            #    vgy = flight_data_dict['vgy']
            #    vgz = flight_data_dict['vgz']
            #    templ = flight_data_dict['templ']
            #    temph = flight_data_dict['temph']
            #    tof = flight_data_dict['tof']
            #    alt = flight_data_dict['alt']
            #    bat = flight_data_dict['bat']
            #    pres = flight_data_dict['pres']
            #    time = flight_data_dict['time']
            #    agx = flight_data_dict['agx']
            #    agy = flight_data_dict['agy']
            #    agz = flight_data_dict['agz']
            #    vel_txt = "Vgx: " + str(vgx) + ", Vgy: " + str(vgy) + ", Vgz: " + str(vgz)
            #    angle_txt = "pitch: " + str(pitch) + ", roll: " + str(roll) + ", yaw: " + str(yaw)
            #    acc_txt =  "agx: " + str(agx) + ", agy: " + str(agy) + ", Vgz: " + str(agz)
            #    misc_txt = "alt: " + str(alt) + ", pres: " + str(pres) + ", Batt: " + str(bat)  +"%"
            #    cv2.putText( frame, vel_txt,   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA )
            #    cv2.putText( frame, angle_txt, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA )
            #    cv2.putText( frame, acc_txt,   (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA )
            #    cv2.putText( frame, misc_txt,  (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA )
            cv2.imshow( "Tello cam", frame )
        else:
            print("No video")
    cap.release()



def get_flight_params( flightdata_queue ):
    fd_lists = flightdata_queue.get().split(';')
    pitch = float( fd_lists[0].split(':')[1] )
    roll  = float( fd_lists[1].split(':')[1] )
    yaw   = float( fd_lists[2].split(':')[1] )
    vgx   = float( fd_lists[3].split(':')[1] )
    vgy   = float( fd_lists[4].split(':')[1] )
    vgz   = float( fd_lists[5].split(':')[1] )
    templ = float( fd_lists[6].split(':')[1] )
    temph = float( fd_lists[7].split(':')[1] )
    tof   = float( fd_lists[8].split(':')[1] )
    alt   = float( fd_lists[9].split(':')[1] )
    bat   = float( fd_lists[10].split(':')[1] )
    pres  = float( fd_lists[11].split(':')[1] )
    time  = float( fd_lists[12].split(':')[1] )
    agx   = float( fd_lists[13].split(':')[1] )
    agy   = float( fd_lists[14].split(':')[1] )
    agz   = float( fd_lists[15].split(':')[1] )
    return { 'pitch': pitch, 'roll': roll, 'yaw': yaw, 'vgx': vgx, 'vgy': vgy,
     'vgz': vgz, 'templ': templ, 'temph': temph, 'tof': tof, 'alt': alt, 
     'bat': bat, 'pres': pres, 'time':time, 'agx': agx, 'agy':agy, 'agz': agz}

if __name__ == '__main__':
    #コマンドを送信したときの返信を受けるキュー
    cmdreq_queue = queue.Queue()
    #フライトデータを受信するキュー
    flight_data_queue = queue.Queue()
    sock_cmd = prep_cmd_socket()
    sock_stat = prep_stat_socket()

    #コマンド送信後の返信を受けるキュー
    recv_cmd_thread = threading.Thread( target=recv_cmd, args= ( cmdreq_queue, sock_cmd ) )
    recv_cmd_thread.start()
    #command命令を送信してモードを変更する
    sock_cmd.sendto( 'command'.encode( encoding='utf-8' ), (TELLO_IP, TELLO_CMD_PORT) )
    #Video streamingを念のため停止しておく
    sock_cmd.sendto( 'streamoff'.encode( encoding='utf-8' ), (TELLO_IP, TELLO_CMD_PORT) )
    #フライトデータを受信するスレッドの作成と開始
    stat_thread = threading.Thread( target = receive_stat, args = ( flight_data_queue, sock_stat ) )
    stat_thread.start()


    #ストリームの開始
    sock_cmd.sendto( 'streamon'.encode( encoding='utf-8' ), (TELLO_IP, TELLO_CMD_PORT) )
    #Videoストリームを受信して，opencvに送る
    video_addr = 'udp://' + LOCAL_IP + ':' + str( TELLO_VIDEO_PORT )
    cap = cv2.VideoCapture( video_addr )
    cap.set(cv2.CAP_PROP_FPS, 15.0)
    cap.set( 3, 320 )
    cap.set( 4, 240 )
    vel_txt   = ""
    angle_txt = ""
    acc_txt   = ""
    misc_txt  = ""
    flight_data_dict = {}

    #Videoストリームを表示するスレッド
    video_display_thread = threading.Thread( target = video_display, args = ( cap, ) )
    video_display_thread.start()

    while True:
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
        elif k == ord('b'):
            send_cmd( 'battery?'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('t'):
            send_cmd( 'takeoff'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('t'):
            send_cmd( 'land'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('8'):
            send_cmd( 'forward 100'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('2'):
            send_cmd( 'back 100'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('6'):
            send_cmd( 'right 100'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('4'):
            send_cmd( 'left 100'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('9'):
            send_cmd( 'cw 10'.encode( encoding='utf-8' ), sock_cmd )
        elif k == ord('7'):
            send_cmd( 'ccw 10'.encode( encoding='utf-8' ), sock_cmd )
        if flight_data_queue.empty()  == False:
            #print( 'LOOP: ' + flight_data.get() )
            flight_data_dict = get_flight_params( flight_data_queue )
            pitch = flight_data_dict['pitch']
            roll = flight_data_dict['roll']
            yaw = flight_data_dict['yaw']
            vgx = flight_data_dict['vgx']
            vgy = flight_data_dict['vgy']
            vgz = flight_data_dict['vgz']
            templ = flight_data_dict['templ']
            temph = flight_data_dict['temph']
            tof = flight_data_dict['tof']
            alt = flight_data_dict['alt']
            bat = flight_data_dict['bat']
            pres = flight_data_dict['pres']
            time = flight_data_dict['time']
            agx = flight_data_dict['agx']
            agy = flight_data_dict['agy']
            agz = flight_data_dict['agz']
            #print( '{pitch}, {roll}, {yaw}, {vgx}, {vgy}, {vgz}, {templ}, {temph}, {tof}, {alt}, {bat}, {pres}, {time}, {agx}, {agy}, {agz}'
            #    .format( pitch=str(pitch), roll=str(roll), yaw=str(yaw), vgx=str(vgx),
            #             vgy=str(vgy), vgz=str(vgz), templ=str(templ),temph=str(temph),
            #             tof=str(tof), alt=str(alt), bat=str(bat), pres=str(pres),
            #             time=str(time), agx=str(agx), agy=str(agy), agz=str(agz) ) )
        if cmdreq_queue.empty()  == False:
            print( 'LOOP: ' + cmdreq_queue.get() )

    #Terminating threads and wait
    recv_cmd_enable = False
    receive_stat_enable = False
    video_display_thread_enabled = False
    recv_cmd_thread.join()
    stat_thread.join()
    video_display_thread.join()
    #Stop streaming
    sock_cmd.sendto( 'streamoff'.encode( encoding='utf-8' ), (TELLO_IP, TELLO_CMD_PORT) )
    #Closing UDP sockets
    sock_stat.close()
    sock_cmd.close()

    cv2.destroyAllWindows()
