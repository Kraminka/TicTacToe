import sys

import random

class Player(object):
	def __init__(self, name):
		self.name = name
		self.human = False
		
class TicTacToe:

	WIN_SET = (
	(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), 
	(1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
	)

	def __init__(self):
		self.finished = False
		self.current_player = 0
		self.players = []
		self.winner = None
		self.move = None

		# ' ', 'x'. 'o'
		self.board = [' '] * 9

	def ready(self):
		return len(self.players) == 2

	def addPlayer(self, playerclass):
		if len(self.players) == 0:
			player = playerclass('X')

			isHuman = input('Human Player? y/n: ')

			if ( isHuman == "y") :
				player.human = True

		else:
			player = playerclass('O')

		self.players.append(player)


	def validateMove(self, move):
		return self.board[int(move)] == ' '


	def getMove(self):
		current_player = self.players[self.current_player]

		if (current_player.human == True):
			move = self.get_human_move()
			
		else:
			#move = self.get_random_ai_move()
			move = self.get_ai_2_move()
					
		return move


	def update(self, move):
		board = self.board

		board[int(move)] = self.players[self.current_player].name

		if self.current_player == 0:
			self.current_player = 1
		else:
			self.current_player = 0

		for winchance in TicTacToe.WIN_SET:
			if board[winchance[0]] is not ' ':
				if board[winchance[0]] == board[winchance[1]] == board[winchance[2]]:
					self.winner = board[winchance[0]]
					self.finished = True

		numfilled = 0
		for tile in board:
			if tile is not ' ':
				numfilled += 1

		if numfilled == 9:
			self.finished = True


	def render(self):
		'''Display the current game board to screen.'''
		board = self.board
		print (""											)
		print ('    %s | %s | %s' % tuple(self.board[:3])	)
		print ('   -----------'								)
		print ('    %s | %s | %s' % tuple(self.board[3:6])	)
		print ('   -----------'								)
		print ('    %s | %s | %s' % tuple(self.board[6:])	)
		print (""											)

		# pretty print the current player name
		if self.winner is None:
			print ('The current player is: %s' % self.players[self.current_player].name)


	def takeTurn(self):
		## Game Loop ##

		#if (self.players[self.current_player].human == True):
		#	self.move = self.get_human_move()

		#else:
		move = self.getMove()

		while not self.validateMove(move):
			move = self.getMove()

		self.update(move)

		self.render()

	#============================================================================================
	# Player and AI Moves

	def get_human_move(self):
		#Get a human players raw input
		return input('[0-8] >> ')

	def get_random_ai_move(self):
		return random.randint(0,8)

	# AI 1: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def get_ai_1_move(self):

		board = self.board

		# if available, go middle.
		if self.validateMove(4):
			return 4

		for winchance in TicTacToe.WIN_SET:

			# Check for own moves O _ _
			if board[winchance[0]] is 'O':
				if board[winchance[1]] == ' ' and self.validateMove(winchance[1]):
					return winchance[1]
				elif board[winchance[2]] == ' ' and self.validateMove(winchance[2]):
					return winchance[2]

			# Check for own moves _ O _
			if board[winchance[1]] is 'O':
				if board[winchance[0]] == ' ' and self.validateMove(winchance[0]):
					return winchance[0]
				elif board[winchance[2]] == ' ' and self.validateMove(winchance[2]):
					return winchance[2]

			# Check for own moves _ _ O
			if board[winchance[2]] is 'O':
				if board[winchance[0]] == ' ' and self.validateMove(winchance[0]):
					return winchance[0]
				elif board[winchance[1]] == ' ' and self.validateMove(winchance[1]):
					return winchance[1]

			# check for moves like x _ x
			if board[winchance[1]] is not 'O':
				if board[winchance[0]] == board[winchance[2]] and self.validateMove(winchance[1]):
					return winchance[1]
			
			# Check for two in a row, like: x x _
			if board[winchance[2]] is not 'O':
				if board[winchance[0]] == board[winchance[1]] and self.validateMove(winchance[2]):
					return winchance[2]

			# Check for two in a row, like: _ x x
			if board[winchance[0]] is not 'O':
				if board[winchance[1]] == board[winchance[2]] and self.validateMove(winchance[0]):
					return winchance[0]

		# For when it can't go in the middle
		return random.randint(0,8)
		
	# AI 1 End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# AI 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# This AI is smarter, and will check if the player can win in the next move, and block it.

	def get_ai_2_move(self):
		
		board = self.board

		for winchance in TicTacToe.WIN_SET:

			if board[winchance[0]] == 'X' and ( board[winchance[1]] == 'X' or board[winchance[2]] == 'X'):
				
				if board[winchance[0]] == board[winchance[1]] and board[winchance[2]] == ' ':
					return winchance[2]

				elif board[winchance[1]] == board[winchance[2]] and board[winchance[0]] == ' ':
					return winchance[0]

				elif board[winchance[0]] == board[winchance[2]] and board[winchance[1]] == ' ':
					return winchance[1]

		
		# For the initial moves #
		# try to go in the middle
		# Otherwise, try a corner
		if self.validateMove(4):
			return 4

		corners = (0,2,6,8)
		move = random.choice(corners)
		return move

	# AI 2 End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	#================================================================================================

	def show_gameresult(self):
		#Show the game result winner/tie details
		if self.winner == 'tie':
			print ('TIE!')
		else:
			print (self.winner + ' is the WINNER!!!')
		print ('Game over. Goodbye')

if __name__ == "__main__":

	game = TicTacToe()

	while not game.ready():
		game.addPlayer(Player)

	while not game.finished:
		game.takeTurn()

	game.show_gameresult()