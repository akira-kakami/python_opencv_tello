#2018.12.09
# Webカメラの動画を表示する
# Threadingを利用して，コマ落ちを防ぐ


import cv2
import threading
video_display_enabled = True
cap = cv2.VideoCapture(0)

def video_display( ):
    while video_display_enabled:
        ret, frame = cap.read()
        if ret:
            cv2.putText(frame, "In camera", (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 1, cv2.LINE_AA )
            cv2.imshow("Webcam", frame)
        else:
            print( "capture read failure")
    


if __name__ == "__main__":
    #cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)
    if cap.isOpened() == False:
        print( "capture initialization read failure")
    else:
        video_display_thread = threading.Thread( target = video_display )
        video_display_thread.start()

    
    while cap.isOpened():      
        k = cv2.waitKey(1)
        if k == ord("q"):
           break

    video_display_enabled = False
    cap.release()   
    cv2.destroyAllWindows()




