from tkinter import *
import tkinter
import time

class KeyboardTk:
	def __init__(self, calling_application):
		self.root_kb = calling_application
		self.buttons = [
		['~','`','!','@','#','$','%','^','&','*','(',')'],
		['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o','p','-','_'],
		['a', 's', 'd', 'f', 'g', 'h','j', 'k', 'l','[',']','BACK'],
		['z', 'x','c','v', 'b', 'n', 'm','\\','/',',', '.','?'],
		[ 'SHIFT', '1','2','3','4','5','7','6','8','9', 'ENTER']
		]
		#'SPACE','SHIFT','ENTER'
		self.enter_pressed = False
		self.button_objects = []

		# self.launch_keyboard()
		# self.update()

	def select(self, value):
		if value == "BACK":
			self.entry.delete(len(self.entry.get())-1,tkinter.END)		
		elif value == "SPACE":
			self.entry.insert(tkinter.END, ' ')
		elif value == " Tab ":
			self.entry.insert(tkinter.END, '    ')
		elif value == "ENTER":
			self.enter_pressed = True
		else :
			self.entry.insert(tkinter.END,value)

	def launch_keyboard(self):
		self.frame = tkinter.Frame(self.root_kb)
		self.frame.pack()
		self.entry = Entry(self.frame, width=30)
		self.entry.pack(side=TOP)
		self.canvas = tkinter.Canvas(self.frame, width=240, height=320)
		self.canvas.pack()
		
		varRow = 20
		varColumn = 0
		for i in range(len(self.buttons)):
			for button in self.buttons[i]:
				command = lambda x=button: self.select(x)
				if (button=='SHIFT' or button=='ENTER'):
					bt = tkinter.Button(self.frame, text=button,width=4, bg="#3c4987", fg="#ffffff",
							activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
							pady=1, bd=1,command=command).place(x=varColumn, y=varRow)
				else:
					bt = tkinter.Button(self.frame, text=button,width=2, bg="#3c4987", fg="#ffffff",
							activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
							pady=1, bd=1,command=command).place(x=varColumn, y=varRow)

				varColumn += 20
			varColumn = 0
			varRow += 20
			
	def update(self):
		if (self.enter_pressed):
			self.remove_keyboard()
		self.frame.after(15, self.update)

	def remove_keyboard(self):
		self.frame.pack_forget()

# root = Tk()
# root.title('kb')
# KeyboardTk(root)
# root.mainloop()