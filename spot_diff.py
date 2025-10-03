import cv2
from skimage.metrics import structural_similarity
import beepy
import utils
import os, datetime
import winsound

def spot_diff(frame1, frame2):
    # ✅ Remove tuple unpacking — assume inputs are already frames (BGR numpy arrays)

    # Convert to grayscale
    if len(frame1.shape) == 3:
        g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    else:
        g1 = frame1

    if len(frame2.shape) == 3:
        g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    else:
        g2 = frame2

    # Slight blur to reduce noise
    g1 = cv2.blur(g1, (2,2))
    g2 = cv2.blur(g2, (2,2))

    # Structural Similarity Index (SSIM)
    score, diff = structural_similarity(g1, g2, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold differences
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # Contour detection (OpenCV 4.x safe)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) > 50]

    # Draw bounding boxes for stolen regions
    if len(contours):
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show results
    cv2.imshow("Stolen", frame1)
    winsound.Beep(1000, 500) #beepy.beep(sound=4)
    

    # Save + send email
    utils.save_frame_with_timestamp(frame1, save_location='stolen')
    utils.email_notify("Stolen found!", frame=frame1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 1
