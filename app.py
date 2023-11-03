import cv2
import numpy as np
import dlib
from imutils import face_utils
import playsound
import math
import time

#cap1=cv2.VideoCapture(0)

def bny(cap,name,threshold_active,threshold_drowsy,road_type):
    
    
    detector = dlib.get_frontal_face_detector()
    predictor= dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    path="alarm2(trimmed).wav"
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    sleep=0
    drowsy=0
    active=0
    yawn_countdown = 0
    status=""
    color=(0,0,0)

    def compute(ptA,ptB):
        dist=np.linalg.norm(ptA-ptB)
        return dist


    def blinked(a,b,c,d,e,f):
        up=compute(b,d)+compute(c,e)
        down=compute(a,f)
        ratio=round((up/(2.0*down)),2)
        if(ratio>threshold_active):
            return 2
        elif(ratio>threshold_drowsy and ratio<=threshold_active):
            return 1
        else:
            return 0


    def yawn(mouth):
        return ((euclideanDist(mouth[2], mouth[10])+euclideanDist(mouth[4], mouth[8]))/(2*euclideanDist(mouth[0], mouth[6])))
    def euclideanDist(a, b):
        return (math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2)))


    while True:
        try:

            ret,frame=cap.read()

            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            faces = detector(gray)
            shape = face_utils.shape_to_np(predictor(frame, faces[0]))

            for face in faces:
                x1=face.left()
                y1=face.top()
                x2=face.right()
                y2=face.bottom()
                
                cv2.putText(frame,"HI ! "+name,(60,400),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
                cv2.putText(frame,"You are driving on "+road_type,(60,450),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
                
                face_frame=frame.copy()
                cv2.rectangle(face_frame, (x1,y1),(x2,y2),(0,255,0),2)

                landmarks=predictor(gray,face)
                landmarks=face_utils.shape_to_np(landmarks)

                left_blink=blinked(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
                right_blink=blinked(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])


                if(yawn_countdown>=75):
                    cv2.putText(frame,"YOU ARE ABOUT TO SLEEP !!!",(150,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)


                if(yawn(shape[mStart:mEnd])>0.6):
                    cv2.putText(frame,"YAWN DETECTED !!!",(200,200),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,255),2)
                    yawn_countdown+=1



                if(left_blink==0 or right_blink==0):
                    sleep+=1
                    drowsy=0
                    active=0
                    if(sleep>6):
                        status="SLEEPING !!!"
                        color=(0,0,255)
                        playsound.playsound(path)
                elif(left_blink==1 or right_blink==1):
                    sleep=0
                    drowsy+=1
                    active=0
                    if(drowsy>6):
                        status="DROWSY !!!"
                        color=(255,0,0)
                else:
                    sleep=0
                    drowsy=0
                    active+=1
                    if(active>6):
                        status="ACTIVE :)"
                        color=(0,255,0)
                cv2.putText(frame,status,(60,150),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)

                for n in range(0,68):
                    (x,y)=landmarks[n]
                    cv2.circle(face_frame,(x,y),1,(255,255,255),-1)
        except Exception as e:
            cv2.putText(frame,"DON'T MOVE YOUR HEAD TOO RAPIDLY !!!",(80,200),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),3)
            time.sleep(0.2)
            print("DON'T MOVE YOUR HEAD TOO RAPIDLY !!!")



        cv2.imshow("Frame: ",frame)
        cv2.imshow("Result of detector: ",face_frame)
        key=cv2.waitKey(1)
        if key==27:
            cap.release()
            cv2.destroyAllWindows()
            break


