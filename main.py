import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os

from in_out import in_out
from motion import motion
from restrict import restrict
from record import record
from find_steal import find_steal
from identify import main_identify
from fight_detection import detect_fight

def create_img_btn(img_name):
    img_btn = Image.open(os.path.join('icons',img_name))
    img_btn = img_btn.resize((50,50), Image.LANCZOS)
    img_btn = ImageTk.PhotoImage(img_btn)
    return img_btn

def create_btn(text, trigger_func, image):
    btn = tk.Button(frame, text=text, height=90, width=180, fg='green', command = trigger_func, image=image, compound='left')
    btn['font'] = tk.font.Font(size=25)
    return btn

root = tk.Tk()
root.title("VigilAI")
root.iconphoto(True, tk.PhotoImage(file=os.path.join('icons', 'cctv.png')))
root.geometry('800x650')

frame = tk.Frame(root)

frame_title = tk.Label(frame, text="VigilAI")
frame_title['font'] = font.Font(size=35, weight='bold', family='Arial')
frame_title.grid(pady=(10,10), column=2)

spy_icon = Image.open(os.path.join('icons','spy.png'))
spy_icon = spy_icon.resize((150,150), Image.LANCZOS)
spy_icon = ImageTk.PhotoImage(spy_icon)
frame_spy_icon = tk.Label(frame, image=spy_icon)
frame_spy_icon.grid(row=1, pady=(5,10), column=2)

btn_img_1 = create_img_btn('steal.png')
btn_img_2 = create_img_btn('rectangle-of-cutted-line.png')
btn_img_3 = create_img_btn('motion.png')
btn_img_4 = create_img_btn('record.png')
btn_img_5 = create_img_btn('exit.png')
btn_img_6 = create_img_btn('in_out.png')
btn_img_7 = create_img_btn('identify.png')
btn_img_8 = create_img_btn('accident.png')
btn_img_9 = create_img_btn('fight.png')

monitor_btn = create_btn(text='Monitor', trigger_func=find_steal, image=btn_img_1)
monitor_btn.grid(row=3, pady=(20,10))

identify_btn = create_btn(text='Identify', trigger_func=main_identify, image=btn_img_7)
identify_btn.grid(row=3, column=2, pady=(20,10))

restrict_btn = create_btn(text='Restrict', trigger_func=restrict, image=btn_img_2)
restrict_btn.grid(row=3, column=3, pady=(20,10))

motion_btn = create_btn(text='Motion', trigger_func=motion, image=btn_img_3)
motion_btn.grid(row=5, pady=(20,10))

in_out_btn = create_btn(text='In Out', trigger_func=in_out, image=btn_img_6)
in_out_btn.grid(row=5, column=2, pady=(20,10))

record_btn = create_btn(text='Record', trigger_func=record, image=btn_img_4)
record_btn.grid(row=5, column=3, pady=(20,10))

exit_btn = create_btn(text='Exit', trigger_func=root.quit, image=btn_img_5)
exit_btn.grid(row=6, column=2, pady=(20,10))

frame.pack()
root.mainloop()
