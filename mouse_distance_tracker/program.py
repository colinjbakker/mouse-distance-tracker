import pyautogui
import tkinter as tk
import screeninfo
import time
import math
import os

from screeninfo import get_monitors

distance = 0
distance_file = "distance.txt"
prev_x, prev_y = pyautogui.position()
m = ()
for x in get_monitors():
	if x.is_primary:
		m = x

def load_distance():
	global distance
	if os.path.exists(distance_file):
		with open(distance_file, "r") as file:
			content = file.read()
			if content:
				try:
					distance = float(content)
				except ValueError:
					print("not a float")

def save_distance():
	with open(distance_file, "w") as file:
		file.write(str(distance))
		print("saved")

def create_gui():
	def track_mouse():
		global distance, prev_x, prev_y
		current_x, current_y = pyautogui.position()
		x_mm = (current_x - prev_x) * m.width_mm / m.width
		y_mm = (current_y - prev_y) * m.height_mm / m.height
		dist = math.sqrt(x_mm**2 + y_mm**2)
		distance += dist
		prev_x, prev_y = current_x, current_y
		root.after(10, track_mouse)

	def show_distance():
		d = math.floor(distance)

		if distance >= 1000:
			distance_label.config(text=f"{d // 1000:.0f}m {d % 1000 // 10:.0f}cm {d % 1000 % 10:.0f}mm")
		elif distance >= 10:
			distance_label.config(text=f"{d % 1000 // 10:.0f}cm {d % 1000 % 10:.0f}mm")
		else:
			distance_label.config(text=f"{d % 1000 % 10:.0f}mm")
		#print(distance)
		root.after(10, show_distance)
	
	def on_closing():
		save_distance()
		root.destroy()
	
	root = tk.Tk()
	root.minsize(250,70)
	root.title("Mouse Distance Tracker")
	distance_label = tk.Label(root, text="0mm", font = ("Terminal", 16))
	distance_label.pack(pady = 20)
	
	
	show_distance()
	track_mouse()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.mainloop()

load_distance()
create_gui()