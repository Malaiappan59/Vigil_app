import cv2
from spot_diff import spot_diff
import utils
import time
from datetime import datetime

def find_contours(thresh):
    """
    Version-compatible findContours for OpenCV 3.x and 4.x
    Returns contours and hierarchy
    """
    opencv_version = cv2.__version__.split('.')
    major_version = int(opencv_version[0])

    if major_version >= 4:
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def find_steal():
    motion_detected = False
    is_start_done = False
    sent = False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    # Read the first frame
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to capture initial frame")
        cap.release()
        return

    frm1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frm2 = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray2 = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(frm1, gray2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Get contours safely
        contours, _ = find_contours(thresh)

        # Filter small contours
        contours = [c for c in contours if cv2.contourArea(c) > 25]

        # Add timestamp on frame
        cv2.putText(frm2, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255), 2)

        # Motion detected
        if len(contours) > 5:
            cv2.putText(thresh, "Motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            motion_detected = True
            is_start_done = False

        # Motion stopped, check for stolen object
        elif motion_detected and len(contours) < 3:
            if not is_start_done:
                start = time.time()
                is_start_done = True

            end = time.time()
            if (end - start) > 4:
                ret, frame2 = cap.read()
                if not ret:
                    print("Failed to capture frame for difference check")
                    break

                x = spot_diff(frame1, frame2)
                if x == 1:
                    print("Stolen found")

                if not sent:
                    utils.save_frame_with_timestamp(frame2, save_location='stolen')
                    utils.email_notify(
                        f"Object stolen is identified in CCTV!",
                        frame=frame2,
                        img_attachment_name='stolen'
                    )
                    sent = True

                cap.release()
                cv2.destroyAllWindows()
                return
        else:
            cv2.putText(thresh, "No motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

        cv2.imshow("Monitor", thresh)

        # Update previous frame
        frm1 = gray2.copy()

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
