#Project 3 Artificial Intelligence
from Tkinter import *
import random

BOARD_WIDTH = BOARD_HEIGHT = 800
RECT_WIDTH = RECT_HEIGHT = BOARD_WIDTH/20.0
FONT = "Times 20 bold"
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_DOWN  = 3
ACTION_UP = 4


class Cell:
	#i and j pos are positions in the board matrix
	def __init__(self,canvas,rect,i_pos,j_pos,x_center,y_center):
		self.rect = rect
		self.canvas = canvas
		self.i = i_pos
		self.j = j_pos
		self.color = "white"
		self.x_cent = x_center
		self.y_cent = y_center
		self.text = None
		self.text_object = None
		self.is_barrier = False #wether or not the cell is passable
		self.goal = None
	def set_fill(self,color):
		self.canvas.itemconfigure(self.rect,fill=color)
		self.color = color
	def fill(self):
		self.canvas.itemconfigure(self.rect,fill="black")
		self.color = "black"
		self.is_barrier = True
	def addText(self,textr, fontp=FONT,s=False):
		if self.text == None or self.text == "S":
			
			self.text_object = self.canvas.create_text(self.x_cent,self.y_cent,text=textr,fill="black",font=fontp)
			self.text = textr
		elif self.text != 'X':
			self.canvas.itemconfigure(self.text_object,font=fontp,fill="black",text=textr)
			self.text = textr
		
		self.canvas.update()
		
		
class Board(Frame):
	def __init__(self,master=None):
		self.board_matrix = []
		Frame.__init__(self,master,width=BOARD_WIDTH,height=BOARD_HEIGHT)
		self.canvas = Canvas(master=self,width=BOARD_WIDTH,height=BOARD_HEIGHT,bg="white")
		self.draw_board()
		self.canvas.pack()
	def get_random_starting_state(self):
		bset = [(i,j) for i in range(20) for j in range(20)]
		s = random.choice(bset)
		s = self.board_matrix[s[0]][s[1]]
		while s.is_barrier:
			s = random.choice(bset)
			s = self.board_matrix[s[0]][s[1]]
		return s
	def draw_board(self):
		row = []
		x1 = 0
		y1 = 0
		
		x2 = x1 + RECT_WIDTH
		y2 = y1 + RECT_HEIGHT
		
		for i in range(20): #Row
			for j in range(20): #Column
				x_center = (x2 + x1)/2.0
				y_center = (y2+ y1)/2.0
				rect = self.canvas.create_rectangle(x1,y1,x2,y2)
				
				rrect = Cell(self.canvas, rect,i,j,x_center,y_center)
				row.append(rrect)
				
				x1 = x2
				x2 += RECT_WIDTH
			self.board_matrix.append(row)
			y1 = y2
			y2 = y2 + RECT_HEIGHT
			x1 = 0
			x2 = x1 + RECT_WIDTH
			row = []
			
		self.fill_random(50)
		self.gen_random_goal()
	
	def is_valid(self,i,j):
		#Tells whether a board value is accurate or not
		if i > 19 or i < 0:
			return False
		if j >19 or j < 0:
			return False
		if self.board_matrix[i][j].is_barrier:
			return False
		return True
	def is_valid_action(self,state,action):
		state_i = state.i
		state_j = state.j
		if action == ACTION_UP:
			return self.is_valid(state_i-1,state_j)
		elif action == ACTION_DOWN:
			return self.is_valid(state_i+1,state_j)
		elif action == ACTION_LEFT:	
			return self.is_valid(state_i,state_j-1)
		elif action == ACTION_RIGHT:
			return self.is_valid(state_i,state_j+1)
			
	def fill_random(self,num=20):
		bset = [(i,j) for i in range(20) for j in range(20)]
		for i in range(num):
			s = random.choice(bset)
			i = s[0]
			j = s[1]
			self.board_matrix[i][j].fill()
	def gen_random_goal(self):
		bset = [(i,j) for i in range(20) for j in range(20)]
		s = random.choice(bset)
		s = self.board_matrix[s[0]][s[1]]
		while s.is_barrier:
			s = random.choice(bset)
			s = self.board_matrix[s[0]][s[1]]
		s.addText("X")
		self.goal = s
			
		
def main():
	root = Tk()
	board = Board(master=root)
	board.pack()
	board.mainloop()
	
	k = board.board_matrix[1][4].addText("K")
if __name__ == "__main__":
	main()