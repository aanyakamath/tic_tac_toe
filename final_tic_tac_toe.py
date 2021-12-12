from flask import Flask
from flask import request
import requests
import random
import ast


board = {}
board['A1'] = '    '
board['A2'] = '    '
board['A3'] = '    '
board['B1'] = '    '
board['B2'] = '    '
board['B3'] = '    '
board['C1'] = '    '
board['C2'] = '    '
board['C3'] = '    '

def printboard(board):
	print('             ')
	print('      1   2   3 ')
	print('                   ')
	print(' C ' + board['C1'] + '|' + board['C2'] + '|' + board['C3'])
	print('     ----------')
	print(' B ' + board['B1'] + '|' + board['B2'] + '|' + board['B3'])
	print('     ----------')
	print(' A ' + board['A1'] + '|' + board['A2'] + '|' + board['A3'])
	print('                   ')

def resetboard(board):
	board['A1'] = '    '
	board['A2'] = '    '
	board['A3'] = '    '
	board['B1'] = '    '
	board['B2'] = '    '
	board['B3'] = '    '
	board['C1'] = '    '
	board['C2'] = '    '
	board['C3'] = '    '

def invalid_move(move, board):
	if move == 'A1' or 'A2' or 'A3' or 'B1' or 'B2' or 'B3' or 'C1' or 'C2' or 'C3':
		if board[move] == '    ':
			return False
		else:
			return True
	else:
		return True

def game_result(board):
	combinations = [['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'], ['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3'], ['A1', 'B2', 'C3'], ['C1', 'B2', 'A3']]
	for combination in combinations:
		if board[combination[0]] == board[combination[1]] == board[combination[2]] == ' X ':
			return (True, ' X ')
		if board[combination[0]] == board[combination[1]] == board[combination[2]] == ' O ':
			return (True, ' O ')
	keys = board.keys()
	for key in keys:
		if board[key] != '    ':  
			return False
	return (True, 'Draw')

def bot_winning_move(board, marker):
	keys = list(board.keys())
	for key in keys:
		if board[key] == '    ':	
			board[key] = marker
			win = game_result(board)
			if win == (True, marker):
				board[key] = '    '
				return key
			else:
				board[key] = '    '
	return False

def player_winning_move(board, marker):
	keys = list(board.keys())
	for key in keys:
		if board[key] == '    ':
			board[key] = marker
			win = game_result(board)
			if win == (True, marker):
				board[key] = '    '
				return key
			else:
				board[key] = '    '
	return False

def random_move(board, moves):
	valid_moves = []
	for move in moves:
		if board[move] == '    ':
			valid_moves.append(move)
	if len(valid_moves) != 0:
		valid_move = random.choice(valid_moves)
		return valid_move
	else:
		return None

def finding_player_move(board, player_marker):
	if player_marker == ' X ':
		marker = 'X'
	else:
		marker = 'O'
	move = input(marker + ', ' + "Enter a move:")
	check = invalid_move(move, board)
	if check == True:
		move = input("Enter a different move:")
	board[move] = player_marker
	 

def finding_bot_move(board, bot_marker, player_marker, corner_moves, remaining_moves):
	result = bot_winning_move(board, bot_marker) 
	if result != False:
		board[result] = bot_marker
		return result
	else:
		result = player_winning_move(board, player_marker)
		if result != False:
			board[result] = bot_marker
			return result
		else:
			if board['B2'] == '    ':
				board['B2'] = bot_marker
				return 'B2'
			else:
				corner_result = random_move(board, corner_moves) 
				if corner_result != None:
					board[corner_result] = bot_marker
					return corner_result
				else:
					result = random_move(board, remaining_moves)
					if result != None:
						board[result] = bot_marker
						return corner_result		

def after_move(board):
	result = game_result(board)
	if result == (True, ' X '):
		print("X has won.")
		game_over = True
		return game_over
	if result == (True, ' O '):
		print("O has won.")
		game_over = True
		return game_over
	if result == (True, 'Draw'):
		print("The game is a draw.")
		game_over = True
		return game_over
	if result == False:
		game_over = False
		return game_over

def replay():
	choice = input("another game? (y,n)")
	if choice == 'y':
		return "replay"
	else:
		return "over"

	
app = Flask("server")

def run_server():
	app.run()


def run_client(game_type, board, player_marker):
	url = "http://127.0.0.1:5000/command"
	move = input("Enter a move:")
	check = invalid_move(move, board)
	if check == True:
		move = input("Enter a different move:")
	dict = {}
	dict['message'] = 'move'
	dict['marker'] = player_marker
	dict['move'] = move
	board[move] = player_marker
	response = requests.post(url, dict)
	print(response.text)
	bot_dict = ast.literal_eval(response.text)
	bot_move = bot_dict["move"]
	bot_marker = bot_dict["marker"]
	board[bot_move] = bot_marker
	printboard(board)
	result = game_result(board)
	if result == (True, 'Draw'):
		print("draw") 

@app.route('/command', methods=["POST"])
def command():
	player_dict = request.form
	print(request.form)
	if player_dict['marker'] == ' X ':
		marker = ' O '
	else:
		marker = ' X '
	player_move = player_dict['move']
	player_marker = player_dict['marker']
	board[player_move] = player_marker
	move = finding_bot_move(board, marker, player_dict['marker'], corner_moves, remaining_moves)
	printboard(board)
	dict = {}
	dict['message'] = 'move'
	dict['marker'] = marker
	dict['move'] = move
	result = game_result(board) 
	return dict

choice = input("Would you like to play against the computer(c), another player(p), against the computer using flask server and client(f), or against another player using flask server and client(b)?:")

if choice == 'c':
	player_marker = input("Would you like to be X or O:")
	if player_marker == 'X':
		bot_marker = ' O '
		player_marker = ' X '
	else:
		bot_marker = ' X '
		player_marker = ' O '


if choice == 'f':
	flask_option = input("Server or client?:")
	if flask_option == 'client':
		client_marker = input("X or O?:")
		if client_marker == 'X':
			client_marker = ' X '
		else:
			client_marker = ' O '

	
if choice == 'c' or 'f':
	printboard(board)
corner_moves = ['A1', 'A3', 'C1', 'C3']
remaining_moves = ['B1', 'A2', 'B3', 'C2']
if choice == 'f':
	repeat = 'y'
	while(True):
		while(True):
			if flask_option == 'client':
				run_client(choice, board, client_marker)
				result = after_move(board)
				if result == True: 
					break
			if flask_option == 'server':
				run_server()
				result = after_move(board)
				if result == True:
					resetboard(board)
					printboard(board)
					break
		if flask_option == 'client':
			result = replay()
			if result != 'replay':
				break
			else:
				resetboard(board)
				printboard(board)

if choice == 'p':
	while(True):
		finding_player_move(board, ' X ')
		printboard(board)
		result = after_move(board)
		if result == True:
			break
		finding_player_move(board, ' O ')
		printboard(board)
		result = after_move(board)
		if result == True:
			break
