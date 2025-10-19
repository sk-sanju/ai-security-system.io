import cv2
import os
import time
from datetime import datetime
from deepface import DeepFace
from playsound import playsound
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ------------------- Configuration -------------------
# Base directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
KNOWN_FACE_PATH = os.path.join(BASE_DIR, "sanju.jpg")
ALARM_SOUND = os.path.join(BASE_DIR, "security_alarm.mp3")
SENDER_EMAIL = "sanjayskpy1@gmail.com"
APP_PASSWORD = "yylf aixp zfdv qjyk"
RECEIVER_EMAIL = "sanjayskpy7@gmail.com"
ALERT_SUBJECT = "EMERGENCY ALERT!"
ALERT_BODY = "Unknown Person Detected by AI Security System"
ALERT_COOLDOWN = 10  # seconds between alerts

# ------------------- Functions -------------------
def capture_photo():
    """Capture a photo from the webcam and return the file path."""
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        print("Error: Could not access camera.")
        cam.release()
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_path = f"captured_{timestamp}.jpg"
    cv2.imwrite(photo_path, frame)
    cam.release()
    return photo_path

def play_alarm():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ALARM_SOUND)
        pygame.mixer.music.play()
        print("🔊 Alarm sound playing...")
    except Exception as e:
        print(f"Error playing alarm sound: {e}")

def send_alert_email(image_path):
    """Send an email alert with the captured image."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = ALERT_SUBJECT
        msg.attach(MIMEText(ALERT_BODY, "plain"))

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_data = f.read()
            img = MIMEImage(img_data, _subtype="jpeg")
            img.add_header("Content-Disposition", "attachment", filename=os.path.basename(image_path))
            msg.attach(img)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Alert email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# ------------------- Main Logic -------------------
print("🔒 AI Security System Started...")
last_alert_time = 0
known_image_path = KNOWN_FACE_PATH

while True:
    photo_path = capture_photo()
    if not photo_path:
        continue

    try:
        # Compare captured image with known face
        result = DeepFace.verify(img1_path=photo_path, img2_path=known_image_path, model_name="VGG-Face", enforce_detection=False)
        verified = result.get("verified", False)
    except Exception as e:
        print(f"Error in face verification: {e}")
        verified = False

    if not verified and (time.time() - last_alert_time > ALERT_COOLDOWN):
        print("⚠️ Unknown person detected!")
        send_alert_email(photo_path)
        play_alarm()
        last_alert_time = time.time()
    else:
        print("✅ Known person detected (SANJU).")

    time.sleep(5)  # Check every 5 seconds