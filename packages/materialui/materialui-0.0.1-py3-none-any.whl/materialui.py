from tkinter import *

class Window(object):

	def __init__(self, title="Untitled", size="300x200", position="absolute"):
		self.root = Tk()
		self.root.title(title)

		if position == "center":
			ws = self.root.winfo_screenwidth()
			hs = self.root.winfo_screenheight()

			s = size.split("x")

			self.width = int(s[0])
			self.height = int(s[1])

			x = ((ws/2) - (self.width/2))
			y = ((hs/2) - (self.height/2))

			self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
		else:
			self.root.geometry(size)

	def show(self):
		self.root.mainloop()