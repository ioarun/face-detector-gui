import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import *
import time
from tkinter import *
import threading

class FaceDetector(threading.Thread):
	def __init__(self, threadID, name, gui):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.gui = gui
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	def run(self):
		while not self.gui.exit:
			x1 = int(self.gui.width / 4)
			y1 = int(self.gui.height / 4)
			x2 = int(self.gui.width * 3 / 4)
			y2 = int(self.gui.height * 3 / 4)
			rect_img = self.gui.frame[y1:y2, x1:x2]
			faces = self.detect_faces(rect_img)
			if len(faces) > 0:
				self.gui.color = 'green'
			else:
				self.gui.color = 'red'

	def detect_faces(self, rect_img):
		# Convert into grayscale
		gray = cv2.cvtColor(rect_img, cv2.COLOR_BGR2GRAY)
		# Detect faces
		faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
		return faces
	      
class FaceDetectorGUI:
	def __init__(self, window, title, video=0):
		self.exit = 0
		# Video Capture Object
		self.video_source = video
		self.video_cam = MyVideoCapture(self.video_source)
		_, self.frame = self.video_cam.get_frame()
		self.width, self.height, _ = self.frame.shape

		# Initial display -------------------------------------------
		self.window = window
		self.window.title(title)
		self.window.protocol("WM_DELETE_WINDOW", self.handle_exit)
		# Create a canvas that can fit the above video source size
		self.canvas = tkinter.Canvas(window, width=self.width, height=self.height)
		self.canvas.pack()
		# Button that lets the user take a snapshot
		self.btn_capture=tkinter.Button(window, text="Capture", width=10, command=self.capture)
		# Button that lets the user take a snapshot
		self.btn_submit=tkinter.Button(window, text="Submit", width=10, command=self.save)
		# Button that lets the user login
		self.btn_login=tkinter.Button(window, text="Login", width=10, command=self.login)
		self.btn_login.pack(anchor=tkinter.CENTER, expand=True)
	
		# Detection related initializations --------------------------
		self.captured_image = None
		self.color = 'red'

		# Threading
		thread1 = FaceDetector(1, "Thread-1", self)
		thread1.start()

		# Loop ----------------------------------------------------------
		self.delay = 15 # milliseconds
		self.update() # called after every self.delay milliseconds
		self.window.mainloop()

	def login(self):
		self.btn_login.pack_forget()
		self.btn_submit.pack(anchor=tkinter.CENTER, expand=True, side=RIGHT)
		self.btn_capture.pack(anchor=tkinter.CENTER, expand=True, side=LEFT)

	def capture(self):
		# Get a frame from the video source
		self.captured_image = self.frame
		print ("Captured.")

	def save(self):
		# Save the captured image
		cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(self.captured_image, cv2.COLOR_RGB2BGR))
		print ("Saved.")
		
	def update(self):
		# --------------------------------------------------------------
		# Get a frame from the video source
		ret, self.frame = self.video_cam.get_frame()

		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
		self.window.after(self.delay, self.update)
	
		# ---------------------------------------------------------------
		# Detection steps
		x1 = int(self.width / 4)
		y1 = int(self.height / 4) - 40
		x2 = int(self.width * 3 / 4)
		y2 = int(self.height * 3 / 4) - 40
		self.draw_rectangle_onscreen(x1, y1, x2, y2, self.color)
		
	def draw_rectangle_onscreen(self, x1, y1, x2, y2, clr):
		self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=clr)

	def handle_exit(self):
		self.window.destroy()
		self.exit = 1

	
class MyVideoCapture:
	def __init__(self, video_source=0):
		self.exit = 0
		# Open the video source
		self.video_device = cv2.VideoCapture(video_source)
		if not self.video_device.isOpened():
			raise ValueError("Unable to open video source", video_source)

		# Get video source width and height
		self.width = self.video_device.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.video_device.get(cv2.CAP_PROP_FRAME_HEIGHT)
		# self.video_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
		# self.video_device.set(cv2.CAP_PROP_FRAME_WIDTH, 320)

	def get_frame(self):
		if self.video_device.isOpened():
			ret, frame = self.video_device.read()
		if ret:
		 	# Return a boolean success flag and the current frame converted to BGR
		 	return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
		else:
			return (ret, None)


	# Release the video source when the object is destroyed
	def __del__(self):
		if self.video_device.isOpened():
			self.video_device.release()
			

FaceDetectorGUI(tkinter.Tk(), "Face Detector GUI")