import random
import pygame
from scores import piecePositionScores, pieceScore
DEPTH = 2

def findRandomMove(validMoves):
	return validMoves[random.randint(0, len(validMoves)-1)]

# Helper caller Min-Max
def findBestMoveMinMax(gs, validMoves):
	global nextMove
	nextMove = None
	findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
	return nextMove

# Helper caller Nega-Max
def findBestMoveNegaMax(gs, validMoves, returnQueue):
	global nextMove
	pygame.display.quit()	
	pygame.display.quit()	
	nextMove = None
	random.shuffle(validMoves)
	findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
	returnQueue.put(nextMove)

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
	for row in range(len(gs.board)):
		for col in range(len(gs.board[row])):
			square = gs.board[row][col]

			if square != "--":
				piecePositionScore = 0
				if square[1] == "N":
					piecePositionScore = piecePositionScores['N'][row][col]
				elif square[1] == "B":
					piecePositionScore = piecePositionScores['B'][row][col]
				elif square[1] == "Q":
					piecePositionScore = piecePositionScores['Q'][row][col]
				elif square[1] == "R":
					piecePositionScore = piecePositionScores['R'][row][col]
				elif square[1] == "P":
					piecePositionScore = piecePositionScores['P'][row][col]
				elif square[1] == "K":
					piecePositionScore = piecePositionScores['K'][row][col]

				if square[0] == "w":
					score += pieceScore[square[1]] + piecePositionScore * .2
				elif square[0] == "b":
					score -= pieceScore[square[1]] + piecePositionScore * .2

	return score