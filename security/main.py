import face_recognition
import cv2
from playsound import playsound
from gtts import gTTS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import pyautogui
import time

# Function to capture a screenshot
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return "screenshot.png"

def play_sound(file_path):
    try:
        # Play the sound file
        playsound(file_path)
    except Exception as e:
        print(f"Error playing sound: {e}")

def send_mail(sender_email, app_password, receiver_email, subject, body, attachments=None):
    # Create the MIME objects
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach additional files (e.g., screenshots)
    if attachments:
        for attachment in attachments:
            with open(attachment, "rb") as attachment_file:
                image_mime = MIMEImage(attachment_file.read(), _subtype="png")
                image_mime.add_header("Content-Disposition", "attachment", filename=attachment)
                message.attach(image_mime)

    # Connect to the SMTP server using the app password
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Example usage
known_face_encodings = []
known_face_names = []

# Example: Load a sample picture and learn how to recognize it
sanju_image = face_recognition.load_image_file("security\sanju.jpg")
sanju_face_encoding = face_recognition.face_encodings(sanju_image)[0]
known_face_encodings.append(sanju_face_encoding)
known_face_names.append("SANJU")

# You can add more known faces similarly

# Get a reference to the webcam (adjust the index if you have multiple cameras)
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # Check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if not any(matches):
            print("Unknown person detected!")
            
            # Capture a screenshot
            screenshot_path = capture_screenshot()
            cv2.imwrite(screenshot_path, frame)
            
            # Send email with screenshot
            send_mail("sanjayskpy1@gmail.com", "vfjl xayh oyad hpqy", "sanjayskpy7@gmail.com", "EMARGENCY ALERT...", "Unknown Person Spotted...", ["screenshot.png"])
            print("mail sended successfully...")
            
            #play Sound
            sound_file_path = "security\security alarm.mp3"  # Replace with the path to your sound file
            play_sound(sound_file_path)
            
            # Wait for a while before capturing the next screenshot
            time.sleep(0)

        # If a match was found, use the first one
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (247, 19, 2),3)

        # Draw a label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
