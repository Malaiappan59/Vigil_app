import cv2
import utils
import time
from datetime import datetime

x1, y1, x2, y2, region_selected, sent = 0, 0, 0, 0, False, False

def select(event, x, y, flags, param):
    global x1, x2, y1, y2, region_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        region_selected = True

def restrict():
    global x1, x2, y1, y2, region_selected, sent
    region_selected = False

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Select a region")
    cv2.setMouseCallback("Select a region", select)

    while True:
        _, frame = cap.read()

        cv2.imshow("Select a region", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or region_selected:
            cv2.destroyAllWindows()
            break

    while True:
        _, frame1 = cap.read()
        _, frame2 = cap.read()

        frame1only = frame1[y1:y2, x1:x2]
        frame2only = frame2[y1:y2, x1:x2]

        diff = cv2.absdiff(frame2only, frame1only)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        diff = cv2.blur(diff, (5, 5))
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.putText(frame1, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255,255,255), 2)

        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x + x1, y + y1), (x + w + x1, y + h + y1), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION", (430, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if not sent:
                utils.save_frame_with_timestamp(frame1, save_location='restricted')
                utils.email_notify("Somebody gets into rectangular restricted area!", frame=frame1)
                sent = True
        else:
            cv2.putText(frame1, "NO-MOTION", (430, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.imshow("Press Q to exit", frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            sent = False
            cap.release()
            cv2.destroyAllWindows()
            break

