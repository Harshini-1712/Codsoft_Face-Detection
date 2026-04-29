import cv2
import tkinter as tk
from PIL import Image, ImageTk
import random

# Load face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start camera
cap = cv2.VideoCapture(0)

# Mood list
moods = ["Happy 😄", "Sad 😢", "Angry 😡", "Sleepy 😴", "Excited 🤩"]

# GLOBAL variables (IMPORTANT 🔥)
frame_count = 0
current_mood = random.choice(moods)

# GUI
window = tk.Tk()
window.title("Smart Mood Detector 😎")

video_label = tk.Label(window)
video_label.pack()

def update_frame():
    global frame_count, current_mood   # 👈 MUST be first line

    ret, frame = cap.read()
    if not ret:
        return

    frame_count += 1

    # Change mood every 50 frames
    if frame_count % 50 == 0:
        current_mood = random.choice(moods)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        cv2.putText(frame, "No Face 😐", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        # USE current mood
        cv2.putText(frame, current_mood, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    # Convert for Tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    video_label.after(10, update_frame)

def exit_app():
    cap.release()
    window.destroy()

exit_btn = tk.Button(window, text="Exit", command=exit_app)
exit_btn.pack()

update_frame()
window.mainloop()