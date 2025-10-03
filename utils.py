import cv2
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import threading

def _save_frame_with_timestamp(frame, save_location):
    """
    Save a given cv2 frame with the current timestamp as the filename.
    
    Parameters:
        frame: cv2 image frame to be saved.
        save_location: directory where the frame will be saved.
        
    Returns:
        saved_filename: filename of the saved frame.
    """
    # Ensure the save location exists, if not create it
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Construct the filename with timestamp
    filename = f"{timestamp}.jpg"
    
    # Save the frame
    save_path = os.path.join(save_location, filename)
    cv2.imwrite(save_path, frame)
    
def _email_notify(email_content, frame=None, img_attachment_name=None):
    sender_email = "malaiappan59@gmail.com"   #Specify here
    sender_password = "siio #### #### ####"    #Specify here

    recipient_emails = ["malaiappansrikanth59@gmail.com"] #Specify here

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_emails)
    message["Subject"] = "VigilAI - Alert"
    email_content = email_content
    message.attach(MIMEText(email_content, "plain"))

    if frame is not None:
        # Attach image
        _, buffer = cv2.imencode('.jpg', frame)
        frame_as_bytes = buffer.tobytes()
        image = MIMEImage(frame_as_bytes, name="image.jpg" if not img_attachment_name else f"{img_attachment_name}.jpg")
        message.attach(image)

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)

        for recipient_email in recipient_emails:
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}!")
    except Exception as e:
        print(str(e))
    finally:
        smtp_server.quit()

def email_notify(email_content, frame=None, img_attachment_name=None):
    thread = threading.Thread(target=_email_notify, args=(email_content, frame, img_attachment_name))
    thread.start()

def save_frame_with_timestamp(frame, save_location):
    thread = threading.Thread(target=_save_frame_with_timestamp, args=(frame, save_location))
    thread.start()
