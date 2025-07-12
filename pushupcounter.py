import cv2
import numpy as np
import time
import pose as pem

cap = cv2.VideoCapture(0)
pTime = 0

detector = pem.poseDetector(detectionCon=0.8)
count = 0
dir = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if lmList and len(lmList) >= 33:
    
        if lmList[31][2] + 50 > lmList[29][2] and lmList[32][2] + 50 > lmList[30][2]:
            angle = detector.findAngle(img, 11, 13, 15) 

            per = np.interp(angle, (210, 90), (0, 100))  
            bar = np.interp(per, (0, 100), (650, 100))

        
            if per >= 95:
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per <= 5:
                if dir == 1:
                    count += 0.5
                    dir = 0

        
            cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (1080, 75),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    
            cv2.putText(img, f'Push Ups: {int(count)}', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        else:
            cv2.putText(img, "Take your position", (400, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (50, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Push Up Counter", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
