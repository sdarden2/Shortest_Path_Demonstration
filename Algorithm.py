#Algorithm class
#Shortest path algorithm: Q-learning 
#By: Sam Darden

from Board import *
import numpy as np
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_DOWN  = 3
ACTION_UP = 4
INNTER_ITER = 500
OUTER_ITER = 1000
y = .7 #Discount rate
alpha = .6 #Learning rate
lamd = .8
EPSILON = .5

timeval = 0.05#.001 #How long to sleep between iterations (in seconds)
import time


def print_matrix(mat):
	for i in mat:
		print i
def main():
	root = Tk()
	board = Board(master=root)
	board.pack()
	#board.mainloop()
	eps = EPSILON
	#Init Q
	Q = np.random.rand(20,20)
	trace = np.zeros((20,20))
	R = np.zeros((20,20))
	goal = board.goal
	R[goal.i][goal.j] = 1.0
	print "Q initial: "
	print_matrix(Q)

	for iter2 in range(OUTER_ITER): #Episodes
		
		erase_board(board,s=True)
		state = board.get_random_starting_state()
		state.set_fill("red")
		action = random.choice(range(1,5))
		print "Episode: %d" %iter2
		while not board.is_valid_action(state,action):
			action = random.choice(range(1,5))
		for iter in range(INNTER_ITER):
			
			#Take action a
			new_i = state_i = state.i
			new_j = state_j = state.j
			if action == ACTION_DOWN:
				new_i +=1
				txt = "\\/"
				action_name = "DOWN"
			elif action == ACTION_UP:
				new_i -=1
				txt = "/\\"
				action_name = "UP"
			elif action == ACTION_LEFT:
				new_j -=1
				txt = "<"
				action_name = "LEFT"
			elif action == ACTION_RIGHT:
				new_j +=1
				txt = ">"
				action_name = "RIGHT"
			Qq = Q[new_i][new_j]	
		
			#Observe r
			
			#Observe s'
			if board.is_valid_action(state,action):
				new_state = board.board_matrix[new_i][new_j]
				new_font = "Times " + str(int(Qq*30)) + " bold"
				state.addText(txt,new_font) #TAke action
				if iter == 0:
					state.set_fill("red")
				if new_state.color != "red":
					new_state.set_fill("green")
				#print "TO end up in state: %d,%d" %(new_state.i,new_state.j)
				#time.sleep(2)
			else:
				print "ERROR!"
			reward = R[new_i][new_j]
			if reward == 1:
				if iter2 > 200:
					time.sleep(1)
				#print "GOAL!!!!"
				break	
			#new_state = board.board_matrix[new_i][new_j]
			new_action_pair = find_best_action(board,Q,new_state,eps)
			new_action = new_action_pair[0]
			new_action_q = new_action_pair[1]
			#print "New action is " + str(new_action)
			
			if new_action == ACTION_UP:
				qpap_i = new_i - 1
				qpap_j = new_j
			elif new_action == ACTION_DOWN:
				qpap_i = new_i + 1
				qpap_j = new_j
			elif new_action == ACTION_RIGHT:
				qpap_i = new_i
				qpap_j = new_j + 1
			elif new_action == ACTION_LEFT:
				qpap_i = new_i
				qpap_j = new_j - 1
				
			Qp = Q[qpap_i][qpap_j]
			
			
			delta = reward + y*Qp - Qq
			trace[new_i][new_j] += 1.0
			
			
			
			for i in range(20):
				for j in range(20):
					cell = board.board_matrix[i][j]
					Q[i][j] = Q[i][j] + alpha*delta*trace[i][j]
					trace[i][j] = y*lamd*trace[i][j]

			"""
			cell = board.board_matrix[new_i][new_j]
			Q[new_i][new_j] = Q[new_i][new_j] + alpha*delta*trace[new_i][new_j]
			trace[new_i][new_j] = y*lamd*trace[new_i][new_j]
			"""
			state = board.board_matrix[new_i][new_j]
			action = new_action
			
			if iter2 > 200:
				time.sleep(timeval)
		
		eps = eps - .01
			
	print "Ending Q: "
	print_matrix(Q)
	board.mainloop()
	
def update_board(board,Q):
	for i in range(20):
		for k in range(20):
			cell = board.board_matrix[i][k]
			if not cell.is_barrier:
				act = find_best_action(board,Q,cell,0)
				new_font = "Times " + str(int(act[1]*30)) + " bold"
				if act[0] == ACTION_UP:
					cell.addText("/\\",new_font)
				elif act[0] == ACTION_DOWN:
					cell.addText("\\/",new_font)
				elif act[0] == ACTION_RIGHT:
					cell.addText(">",new_font)
				elif act[0] == ACTION_LEFT:
					cell.addText("<",new_font)
def erase_board(board,s=False):
	for i in range(20):
		for j in range(20):
			cell = board.board_matrix[i][j]
			"""
			if s == True and cell.text == "S":
				print "Condition true!"
				cell.addText("",s=True)
			if not (cell.is_barrier or cell.text == "X" or cell.text=="S"):
				cell.addText("")
			"""	
			if cell.color == "red" or cell.color == "green":
				cell.set_fill("white")
				
				

def find_best_action(board,q,sp,eps):
	a_list = []
	i = sp.i
	j = sp.j
	
	if board.is_valid_action(sp,ACTION_UP):
		a_list.append((ACTION_UP,q[i-1][j]))
	if board.is_valid_action(sp,ACTION_DOWN):
		a_list.append((ACTION_DOWN,q[i+1][j]))
	if board.is_valid_action(sp,ACTION_RIGHT):
		a_list.append((ACTION_RIGHT,q[i][j+1]))
	if board.is_valid_action(sp,ACTION_LEFT):
		a_list.append((ACTION_LEFT,q[i][j-1]))
	if random.random < eps:
		return random.choice(a_list)
	else:
		return (max(a_list,key=lambda x:x[1]))
			
		
	
if __name__ == "__main__":
	main()
		