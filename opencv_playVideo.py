import cv2


if __name__ == '__main__':
    cap = cv2.VideoCapture( "arcjet.mp4" )

    while( cap.isOpened() ):
        ret, frame = cap.read()
        cv2.imshow( "", frame )
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
