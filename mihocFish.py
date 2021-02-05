import random

pieceScore = {"K":0, "Q":9, "R":5, "B":3, "N":3, "P":1}

def findRandomMove(validMoves):
	return validMoves[random.randint(0, len(validMoves)-1)]

# Greedy small scale Min-Max Algorithm
def findGreedyMove(gs, validMoves):
	turnMultiplier = 1 if gs.whiteToMove else -1
	playerMinMaxScore = 1000
	bestAIMove = None
	random.shuffle(validMoves)
	for AIMove in validMoves:
		gs.makeMove(AIMove)
		playerMoves = gs.getValidMoves()
		playerMaxScore = -1000
		for playerMove in playerMoves:
			gs.makeMove(playerMove)
			if gs.checkMate:
				score = -turnMultiplier * 1000
			elif gs.staleMate:
				score = 1
			#elif gs.inCheck():
				#score = -turnMultiplier * 1
			else:
				score = -turnMultiplier *  scoreMaterial(gs.board)
			if score > playerMaxScore:
				playerMaxScore = score
			gs.undoMove()
		if playerMinMaxScore > playerMaxScore:
			playerMinMaxScore = playerMaxScore
			bestAIMove = AIMove
		gs.undoMove()
	return bestAIMove

# Find a way to score the board
def scoreMaterial(board):
	score = 0
	for row in board:
		for square in row:
			if square[0] == "w":
				score += pieceScore[square[1]]
			elif square[0] == "b":
				score -= pieceScore[square[1]]

	return score