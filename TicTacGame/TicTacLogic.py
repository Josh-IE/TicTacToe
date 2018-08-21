from rest_framework import renderers

class Board:
	media_type = 'text/plain'
	format = 'txt'

	def __init__(self, board_string_req, player_wave, player_api, blank):
		self.board_string_req = board_string_req
		self.player_wave = player_wave
		self.player_api = player_api
		self.blank = blank
		self.valid_board_string_chars = [self.player_wave, self.player_api, self.blank]
		self.didWin = False

		#build game matrix
		self.matrix = self.build_matrix()

	def validBoard(self):
		#check for invalid chars
		for x in self.board_string_req:
			if x not in self.valid_board_string_chars:
				return False

		#check board char count. This must == 9
		if len(self.board_string_req) != 9:
			return False

		#check if current board state is valid tictac based on char count
		count_x = self.board_string_req.count(self.player_wave)
		count_o = self.board_string_req.count(self.player_api)
		if count_x - count_o not in [0, 1]:
			return False
		
		#check if game is already won
		if self.game_won():
			return False 

		return True

	def makeMove(self):
		"""
		STRATEGY: Ordered by priority
		1. Check for a winning play and finish it. If none, continue
		2. Check for 2nd player(Wave server) winning play and block it. If non continue
		3. check positions of characters on the board, and strategize a move
			occupy center, if not occupied
				occupy a corner, that has a free adjacent corner
					occupy the adjacent corner
					finish the winning move (along the corner row, diagonally left. diagonally right)
				if none, play along diagonal or middle if clear
			occupy a corner position that has a free adjacent corner, if center is occupied
				ocuupy the opposite corner(along diagonal)
				occupy a corner adjacent to both corners
				finish the winning move my occupying a free edge
			game is in gridlock
				play random
		"""
		#finish a winning move
		self.playWin()
		if self.didWin:
			return self.stringifyMatrix()
		else:
			#check for wave winning move and block it
			#time is up. return any play
			self.playAny()
			return self.stringifyMatrix()

	def build_matrix(self):
		fst_row = []
		snd_row = []
		thd_row = []
		board_str_counter = 0
		for x in self.board_string_req:
			if board_str_counter in [0, 1, 2]:
				fst_row.append(x)
			elif board_str_counter in [3, 4, 5]:
				snd_row.append(x)
			elif board_str_counter in [6, 7, 8]:
				thd_row.append(x)
			board_str_counter+=1
		return [
			fst_row,
			snd_row,
			thd_row
		]
	
	#check if game is won
	def game_won(self):
		#check rows
		for i in range(0, 2):
			if self.matrix[i][0] != ' ' and self.matrix[i][1] == self.matrix[i][0] and self.matrix[i][2] == self.matrix[i][1]:
				return True
		#check cols
		for i in range(0, 2):
			if self.matrix[0][i] != ' ' and self.matrix[0][i] == self.matrix[1][i] and self.matrix[2][i] == self.matrix[1][i]:
				return True
		#check diagonals
		if self.matrix[0][0] != ' ' and self.matrix[0][0] == self.matrix[1][1] and self.matrix[2][2] == self.matrix[1][1]:
			return True
		if self.matrix[0][2] != ' ' and self.matrix[0][2] == self.matrix[1][1] and self.matrix[2][0] == self.matrix[1][1]:
			return True
		return False
	
	#finish a winnning move
	def playWin(self):
		#check for a winning move across the rows		
		for i in range(len(self.matrix)):
			count = 0
			counter = 0
			row = col = None
			for j in range(len(self.matrix)):				
				if self.matrix[i][j] == self.player_api:
					count+=1
				elif self.matrix[i][j] == self.player_wave:
					count-=1
				else:
					row = i
					col = j
				print (count)
				counter += 1
				if count == 2 and counter == 3:
					#insert self.player_api in blank space
					self.matrix[row][col] = self.player_api
					self.didWin = True
					break
			else:
				continue
			break
		if self.didWin == True:
			return
		#check for a winning move along the cols
		for i in range(len(self.matrix)):
			current_col = [self.matrix[0][i], self.matrix[1][i], self.matrix[2][i]]
			if current_col.count(self.player_api) == 2 and current_col.count(self.player_wave) == 0:
				#find index of blank
				blank_index = current_col.index(self.blank)
				#insert into blank
				self.matrix[blank_index][i] = self.player_api
				self.didWin = True
				break
	
		#check for a winning move along the diagonals


	def stringifyMatrix(self):
		play_string = ''
		for row in self.matrix:
			for col in row:
				play_string+=col
		return play_string

	def playAny(self):
		if self.matrix[0][0] == self.blank:
			self.matrix[0][0] = self.player_api
		elif self.matrix[0][1] == self.blank:
			self.matrix[0][1] = self.player_api
		elif self.matrix[0][2] == self.blank:
			self.matrix[0][2] = self.player_api
		elif self.matrix[1][0] == self.blank:
			self.matrix[1][0] = self.player_api
		elif self.matrix[1][1] == self.blank:
			self.matrix[1][1] = self.player_api
		elif self.matrix[1][2] == self.blank:
			self.matrix[1][2] = self.player_api
		elif self.matrix[2][0] == self.blank:
			self.matrix[2][0] = self.player_api
		elif self.matrix[2][1] == self.blank:
			self.matrix[2][1] = self.player_api
		elif self.matrix[2][2] == self.blank:
			self.matrix[2][2] = self.player_api





		