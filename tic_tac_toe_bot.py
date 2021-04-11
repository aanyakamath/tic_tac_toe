
#Used in random generating bot_move function (later on)
import random

#Checks if player moves are valid
#Makes sure player moves are spaces on the board
#Makes sure players do not move into occupied squares
#Run after every players move
def invalidcheck(a,b):
	if a == "A1" or "A2" or "A3" or "B1" or "B2" or "B3" or "C1" or "C2" or "C3":
		if b == "    ":
			return "1"
		else:
			return "0"
	else:
		return "0"

#Checks if game is over
#Gets run after every player makes their move
#Checks if game is over, and returns player that has won or returns "draw"
def is_game_over_3(board):
	wins = [['A1', 'A2', 'A3',], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'], ['C1', 'B1', 'A1'], ['C2', 'B2', 'A2'], ['C3', 'B3', 'A3'], ['C1', 'B3', 'A3'], ['C3', 'B2', 'A1']]
	for win in wins:
		if board[win[0]] == board[win[1]] == board[win[2]]:
			if board[win[0]] != "    ":
				return board[win[0]]

	spaces = list(board.keys())
	for space in spaces:
		if board[space] == "    ":
			return "Not Over."

	return "Draw."

#If there is a move resulting in the bot winning, this function finds it
#Returns that move, and when function runs, bot plays the move, and wins
def get_bot_winning_move_2(board):
	spaces = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
	for i in spaces:
		if board[i] == "    ":
			board[i] = ' O '
			x = is_game_over_3(board)
			if x == (' O '):
				return i
			else:
				board[i] = "    "

	return "False"

#If there is a move resulting in the bot's oponent winning, this function finds it
#Returns that move, and when function runs, bot plays the move, and stops oponent from winning
def get_plyr_win_2(board):
	spaces = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
	for i in spaces:
		if board[i] == "    ":
			board[i] = ' X '
			x = is_game_over_3(board)
			if x == (' X '):
				return i
			else:
				board[i] = "    "

	return "False"


def random_bot_move(board):
	board_list = list(board.keys())
	random_piece_choice = random.choice(board_list)
	while(True):
		if board[random_piece_choice] == "    ":
			return random_piece_choice
			break
		else:
			random_piece_choice = random.choice(board_list)


#Prints the board using the dictionary below
def printboard(): 
	print('              ')
	print(board['C1'] + '|' + board['C2'] + '|' + board['C3'])
	print('--------------')
	print(board['B1'] + '|' + board['B2'] + '|' + board['B3'])
	print('--------------')
	print(board['A1'] + '|' + board['A2'] + '|' + board['A3'])
	print('              ')

#Dictionary represents the spaces on the board
board = {}
board["A1"] = "    "
board["A2"] = "    "
board["A3"] = "    "
board["B1"] = "    "
board["B2"] = "    "
board["B3"] = "    "
board["C1"] = "    "
board["C2"] = "    "
board["C3"] = "    "

#Asks player if wants to play with computer or other player
game_type = input("Do you want to play against the computer (c)? Or against another player (p)?: ")

#Ask player if wants to play X or O
if game_type == 'c':
	playername = input("Would you like to be X or O?")
if game_type == 'p':
	playerX = input("Who is Player X?")
	playerO = input("Who is Player O?")

#For Loop is designed to keep iterating until both players have played their moves until either player wins, or the game is a draw.
#While Loops go through the process of getting each players move, checking if its valid, inputing it into the board, and checking if the game is over
game_over = False
printboard()
for i in range(9):
	if game_type == 'c':
		while(True):
			playermove = input(playername + ", what's your move?")
			invalidresult = invalidcheck(playermove, board[playermove])
			if invalidresult == "0":
					print(playername + ", please redo your move.")
			if invalidresult == "1":
					board[playermove] = ' X '
					printboard()
			gameoverresult = is_game_over_3(board)
			if gameoverresult == (' X '):
				print("X has won.")
				game_over = True
				break
			else:
				if gameoverresult == (' O '):
					print("O has won.")
					game_over = True
					break
				else:
					if gameoverresult == "Draw.":
						print("The game is a draw.")
						game_over = True
						break
					else:
						game_over = False
						break

	if game_over == True:
		break

	if game_type == 'p':
		while(True):
			playerXmove = input(playerX + ", what's your move?")
			invalidresult = invalidcheck(playerXmove, board[playerXmove])
			if invalidresult == "0":
				print(playerX + ", please redo your move.")
			if invalidresult == "1":
				board[playerXmove] = ' X '
			printboard()
			gameoverresult = is_game_over_3(board)
			if gameoverresult == (' O '):
				print("O has won.")
				game_over = True
				break
			else:
				if gameoverresult == (' X '):
					print("X has won.")
					game_over = True
					break
				else:
					if gameoverresult == "Draw.":
						print("The game is a draw.")
						game_over = True
						break
					else:
						game_over = False
						break

	if game_over == True:
		break

	if game_type == 'p':
		while(True):
			playerOmove = input(playerO + ", what's your move?")
			invalidresult = invalidcheck(playerOmove, board[playerOmove])
			if invalidresult == "0":
				print(playerO + ", please redo your move.")
			if invalidresult == "1":
				board[playerOmove] = ' O '
			printboard()
			gameoverresult = is_game_over_3(board)
			if gameoverresult == (' O '):
				print("O has won.")
				game_over = True
				break
			else:
				if gameoverresult == (' X '):
					print("X has won.")
					game_over = True
					break
				else:
					if gameoverresult == "Draw.":
						print("The game is a draw.")
						game_over = True
						break
					else:
						game_over = False
						break


	if game_type == 'c':
		while(True):
			bot_win_move = get_bot_winning_move_2(board)
			if bot_win_move != "False":
				board[bot_win_move] = ' O '
				printboard()
			else:
				plyr_win_move = get_plyr_win_2(board)
				if plyr_win_move != "False":
					board[plyr_win_move] = ' O '
					printboard()
				else:
					final_bot_move = random_bot_move(board)
					board[final_bot_move] = " O "
					printboard()
			gameoverresult = is_game_over_3(board)
			if gameoverresult == (' X '):
				print("X has won.")
				game_over = True
				break
			else:
				if gameoverresult == (' O '):
					print("O has won.")
					game_over = True
					break
				else:
					if gameoverresult == "Draw.":
						print("The game is a draw.")
						game_over = True
						break
					else:
						game_over = False
						break
		if game_over == True:
			break

