import threading
import time
from msvcrt import getch

CTRL_C = 3

def funcA ():
    while( funcA_enable == 1):
        print("funcA")
        time.sleep(0.25)

def funcB ():
    while( funcB_enable == 1):
        print("funcB")
        time.sleep(1.0)

if __name__ == "__main__":
    funcA_enable = 1
    funcB_enable = 1
    threadA = threading.Thread( target = funcA )
    threadB = threading.Thread( target = funcB )

    threadA.start()
    threadB.start()
    while True:
        time.sleep(0.05)
        k = ord( getch() ) #文字をUnicodeに変換する．
        if k == CTRL_C:
            break
        else:
            print('input key=0x{:x}'.format( k ) )

    funcA_enable = 0
    funcB_enable = 0
    print("FINISHED")
