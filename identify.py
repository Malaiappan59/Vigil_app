import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog
import utils
from datetime import datetime

def collect_data():
	name = simpledialog.askstring("Input", "Enter name of person:")
	ids = simpledialog.askstring("Input", "Enter the ID:")

	filename = "haarcascade_frontalface_default.xml"
	cascade = cv2.CascadeClassifier(filename)

	count = 1
	cap = cv2.VideoCapture(0)

	while True:
		_, frm = cap.read()

		gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
		faces = cascade.detectMultiScale(gray, 1.4, 1)

		for x,y,w,h in faces:
			cv2.rectangle(frm, (x,y), (x+w, y+h), (0,255,0), 2)
			roi = gray[y:y+h, x:x+w]

			cv2.imwrite(f"persons/{name}-{count}-{ids}.jpg", roi)
			count = count + 1
			cv2.putText(frm, f"{count}", (20,20), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
			cv2.imshow("new", roi)

		cv2.imshow("Train face", frm)

		if cv2.waitKey(1) & 0XFF == ord('q') or count > 100:
			cv2.destroyAllWindows()
			cap.release()
			train()
			break

def train():
	tk.messagebox.showinfo("Info", "Training initiated!")

	recog = cv2.face.LBPHFaceRecognizer_create()

	dataset = 'persons'

	paths = [os.path.join(dataset, im) for im in os.listdir(dataset)]

	faces = []
	ids = []
	labels = []
	for path in paths:
		labels.append(path.split('/')[-1].split('-')[0])
		ids.append(int(path.split('/')[-1].split('-')[2].split('.')[0]))
		faces.append(cv2.imread(path, 0))

	recog.train(faces, np.array(ids))
	recog.save('model.yml')

	tk.messagebox.showinfo("Info", "Training completed!")
	return

def identify():
	recog = cv2.face.LBPHFaceRecognizer_create()
	try:
		recog.read('model.yml')
	except:
		tk.messagebox.showwarning("Warning", "No known present!")
		return

	cap = cv2.VideoCapture(0)

	filename = "haarcascade_frontalface_default.xml"

	paths = [os.path.join("persons", im) for im in os.listdir("persons")]
	labelslist = {}
	for path in paths:
		labelslist[path.split('/')[-1].split('-')[2].split('.')[0]] = path.split('/')[-1].split('-')[0]

	cascade = cv2.CascadeClassifier(filename)
	sent = False
	while True:
		_, frm = cap.read()

		cv2.putText(frm, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255,255,255), 2)

		gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

		faces = cascade.detectMultiScale(gray, 1.3, 2)

		for x,y,w,h in faces:
			cv2.rectangle(frm, (x,y), (x+w, y+h), (0,255,0), 2)
			roi = gray[y:y+h, x:x+w]

			label = recog.predict(roi)
			label_ = labelslist[str(label[0])]
			label_ = label_.split('\\')[-1]
			# int(label[1])
			if label[1] < 100:
				cv2.putText(frm, label_, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
				if not sent:
					utils.save_frame_with_timestamp(frm, save_location='identified')
					utils.email_notify(f"Person '{label_}' is identified in CCTV!", frame=frm, img_attachment_name='identified')
					sent = True
			else:
				cv2.putText(frm, "unknown", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

		cv2.imshow("identify", frm)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			cap.release()
			break

def main_identify():
	root = tk.Tk()

	root.geometry("480x100")
	root.title("Identify Options")

	label = tk.Label(root, text="Select your choice")
	label.grid(row=0, columnspan=2)
	label['font'] = tk.font.Font(size=35, weight='bold',family='Arial')

	btn_font = tk.font.Font(size=25)

	button1 = tk.Button(root, text="Add Member", command=collect_data, height=2, width=20)
	button1.grid(row=1, column=0, pady=(10,10), padx=(5,5))
	button1['font'] = btn_font

	button2 = tk.Button(root, text="Start with known", command=identify, height=2, width=20)
	button2.grid(row=1, column=1,pady=(10,10), padx=(5,5))
	button2['font'] = btn_font
	root.mainloop()

	return