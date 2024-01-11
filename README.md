<h1>AI Security System</h1>
<p>This Python script implements a basic face recognition and security system using the face_recognition, cv2 (OpenCV), playsound, gtts (Google Text-to-Speech), and smtplib libraries. The system captures video frames from the webcam, detects faces, and compares them with known faces to determine if an unknown person is present.</p>

<h1>Features</h1>
<h2>Face Recognition:</h2>

<p>The system recognizes faces by comparing them with known faces using facial recognition algorithms.
Known faces are pre-registered with their corresponding encodings.</p>
<h2>Email Notification:</h2>

<p>When an unknown person is detected, the system captures a screenshot and sends an email with the screenshot attached.
The email includes a subject, body, and optional attachments (e.g., screenshot).</p>
<h2>Screenshot Capture:</h2>

<p>Utilizes the pyautogui library to capture a screenshot when an unknown face is detected.</p>
<h2>Video Display:</h2>

<p>Displays the real-time video feed from the webcam with rectangles around detected faces and their corresponding names.</p>
<h2>User Interaction:</h2>

<p>Press 'q' to exit the video feed window and terminate the script.</p>
<h2>Dependencies</h2>
<p>Python 3.x
Required Python libraries: face_recognition, cv2, playsound, gtts, smtplib, pyautogui</p>
<h2>Usage</h2>
1. Install the required libraries:

<h4>bash</h4>
pip install face_recognition opencv-python playsound gtts pyautogui

2. Set up a Gmail account and enable "Less secure app access" to allow the script to send emails.

3. Update the script with your Gmail sender and receiver email addresses, app password, and the paths to the known faces' images.

4. Run the script:

<h4>bash</h4>
python main.py

5. Press 'q' to exit the video feed window and terminate the script.

<h1>Note</h1>
<p>Make sure to keep your Gmail app password secure and do not share it with others.
The script may need adjustments based on the number of cameras connected to your system.
Feel free to customize the script according to your specific requirements and security considerations.</p>
