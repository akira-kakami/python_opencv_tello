import cv2
import threading
     
    


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while cap.isOpened():      
        ret, frame = cap.read()
        if ret:
            cv2.putText(frame, "In camera", (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 1, cv2.LINE_AA )
            cv2.imshow("Webcam", frame)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break;    
    cap.release()   
    cv2.destroyAllWindows()




