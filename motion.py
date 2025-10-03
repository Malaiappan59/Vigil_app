import cv2 
import utils
import time
from datetime import datetime

sent = False

def motion():
    global sent
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    while True:
        _, frame1 = cap.read()
        _, frame2 = cap.read()

        diff = cv2.absdiff(frame2, frame1)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        diff = cv2.blur(diff, (5,5))
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.putText(frame1, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255,255,255), 2)

        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame1, "MOTION", (430,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            if not sent:
                utils.save_frame_with_timestamp(frame1, save_location='motion')
                utils.email_notify("Somebody gets into restricted area!", frame=frame1)
                sent = True
        else:
            cv2.putText(frame1, "NO-MOTION", (430,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("Press Q to exit", frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

