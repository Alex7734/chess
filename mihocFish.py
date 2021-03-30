import random

pieceScore = {"K":0, "Q":9, "R":5, "B":3, "N":3, "P":1}
DEPTH = 2
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
		if gs.staleMate:
			playerMaxScore = 0
		elif gs.checkMate:
			playerMaxScore = -1000
		else:
			playerMaxScore = -1000
			for playerMove in playerMoves:
				gs.makeMove(playerMove)
				gs.getValidMoves()
				if gs.checkMate:
					score = 1000
				elif gs.staleMate:
					score = 1
				elif gs.inCheck():
					score = 1
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

# Helper caller Min-Max
def findBestMoveMinMax(gs, validMoves):
	global nextMove
	nextMove = None
	findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
	return nextMove

# Helper caller Nega-Max
def findBestMoveNegaMax(gs, validMoves):
	global nextMove
	nextMove = None
	random.shuffle(validMoves)
	findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
	return nextMove

# Min-Max Alogorithm
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
	global nextMove
	if depth == 0:
		return scoreBoard(gs, gs.board)

	if whiteToMove:
		maxScore = -1000
		for move in validMoves:
			gs.makeMove(move)
			nextMoves = gs.getValidMoves()
			score = findMoveMinMax(gs, nextMoves, depth-1, False)
			if score > maxScore:
				maxScore = score
				if depth == DEPTH:
					nextMove = move
			gs.undoMove()
		return maxScore
	else:
		minScore = 1000
		for move in validMoves:
			gs.makeMove(move)
			nextMoves = gs.getValidMoves()
			score = findMoveMinMax(gs, nextMoves, depth-1, True)
			if score < minScore:
				minScore = score
				if depth == DEPTH:
					nextMove = move
			gs.undoMove()
		return minScore

# Nega-Max Algorithm
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
	global nextMove
	if depth == 0:
		return turnMultiplier * scoreBoard(gs, gs.board)
	
	maxScore = -1000
	for move in validMoves:
		gs.makeMove(move)
		nextMoves = gs.getValidMoves()
		score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
	
		if score > maxScore:
			maxScore = score
			if depth == DEPTH:
				nextMove = move

		gs.undoMove()

	return maxScore

# Scoring the board
def scoreBoard(gs, board):
	if gs.checkMate:
		if gs.whiteToMove:
			return -1000
		else:
			return 1000

	elif gs.staleMate:
		return 0

	score = 0
	for i, row in enumerate(board):
		for square in row:
			if square[0] == "w":
				score += pieceScore[square[1]]
			elif square[0] == "b":
				score -= pieceScore[square[1]]

	return score