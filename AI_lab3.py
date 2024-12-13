import cv2
import pytesseract
from tkinter import Tk, Label, Button, Frame, Text, Scrollbar, VERTICAL, END
from threading import Thread
from PIL import Image, ImageTk


class TextRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Recognition from Webcam")

        self.video_capture = None
        self.running = False

        # UI Components
        self.video_frame = Label(root)
        self.video_frame.pack(pady=10)

        self.history_frame = Frame(root)
        self.history_frame.pack(pady=10, fill="both", expand=True)

        self.scrollbar = Scrollbar(self.history_frame, orient=VERTICAL)
        self.scrollbar.pack(side="right", fill="y")

        self.text_history = Text(self.history_frame, wrap="word", yscrollcommand=self.scrollbar.set, height=10)
        self.text_history.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.text_history.yview)

        self.control_frame = Frame(root)
        self.control_frame.pack(pady=10)

        self.start_button = Button(self.control_frame, text="Start Webcam", command=self.start_webcam)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = Button(self.control_frame, text="Stop Webcam", command=self.stop_webcam, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)

    def start_webcam(self):
        self.video_capture = cv2.VideoCapture(0)
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.update_frame()

    def stop_webcam(self):
        self.running = False
        if self.video_capture:
            self.video_capture.release()
        self.video_frame.config(image="")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.video_capture.read()
        if not ret:
            self.stop_webcam()
            return

        # Convert the frame to RGB for Tkinter compatibility
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)

        # Process the frame for text recognition in a separate thread
        Thread(target=self.process_text, args=(frame,)).start()

        # Schedule the next frame update
        self.root.after(10, self.update_frame)

    def process_text(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_frame, lang='eng')
        

        if text.strip():
            self.text_history.insert(END, text + "\n")
            self.text_history.see(END)

    def on_closing(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Update path as needed

    root = Tk()
    app = TextRecognitionApp(root)
    root.mainloop()
