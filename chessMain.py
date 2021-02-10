import pygame as pg 
import chessEngine as cE
import mihocFish as AI

pg.init()
WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

def loadImages():
	pieces = ['wP', 'wR', 'wB', 'wN', 'wQ', 'wK', 'bP', 'bR', 'bB', 'bN', 'bK', 'bQ']
	for piece in pieces:
		IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()
	screen.fill(pg.Color("white"))
	gs = cE.GameState()
	loadImages()
	running = True
	sqSelected = ()
	playerClicks = []
	validMoves = gs.getValidMoves()
	moveMade = False
	animate = False
	gameOver = False
	playerOne = True 
	playerTwo = False

	while running:
		humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

		# pygame events 
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

			elif e.type == pg.MOUSEBUTTONDOWN:
				if not gameOver and humanTurn:
					location = pg.mouse.get_pos()
					col = location[0]//SQ_SIZE
					row = location[1]//SQ_SIZE
					if sqSelected == (row, col):
						sqSelected = ()
						playerClicks = []
						moveMade = False
					else:
						sqSelected = (row, col)
						playerClicks.append(sqSelected)
					if len(playerClicks) == 2:
						move = cE.Move(playerClicks[0], playerClicks[1], gs.board)
						for i in range(len(validMoves)):
							if move == validMoves[i]:
								gs.makeMove(validMoves[i])
								moveMade = True
								animate = True
								sqSelected =()
								playerClicks = []
						if not moveMade:
							playerClicks = [sqSelected]

			elif e.type == pg.KEYDOWN:
				if e.key == pg.K_z:
					gs.undoMove()
					moveMade = True
					animate = False
				if e.key == pg.K_r:
					gs = ce.GameState()
					validMoves = gs.getValidMoves()
					sqSelected = ()
					playerClicks = []
					moveMade = False
					animate = False
					gameOver = False

		# AI decision
		if not gameOver and not humanTurn:
			AIMove = AI.findBestMoveNegaMax(gs, validMoves)
			if AIMove is None:
				AIMove = AI.findRandomMove(validMoves)
			gs.makeMove(AIMove)
			moveMade = True
			animate = True

		# Human decision
		if moveMade:
			if animate:
				animateMove(gs.moveLog[-1], screen, gs.board, clock)
			validMoves= gs.getValidMoves()
			moveMade = False
			animate = False

		drawGameState(screen, gs, validMoves, sqSelected)

		# Check end of game
		if gs.checkMate:
			gameOver = True
			if gs.whiteToMove:
				drawText(screen, 'Black wins by checkmate!')
			else:
				drawText(screen, 'White wins by checkmate!')
		elif gs.staleMate:
			gameOver = True
			drawText(screen, 'Stalemate')

		clock.tick(MAX_FPS)
		pg.display.flip()

def drawGameState(screen, gs, validMoves, sqSelected):
	drawBoard(screen)
	highlightSquares(screen, gs, validMoves, sqSelected)
	drawPieces(screen, gs.board)

def highlightSquares(screen, gs, validMoves, sqSelected):
	if sqSelected != ():
		r, c = sqSelected
		if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
			s = pg.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(100)
			s.fill(pg.Color('blue'))
			screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
			s.fill(pg.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawBoard(screen):
	colors = [(235, 235, 208), (119, 148, 85)]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c)%2)]
			pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != "--":
				screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):

	colors = [(235, 235, 208), (119, 148, 85)]	
	cords = []
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framesPerSquare = 10 
	frameCount = (abs(dR) + abs(dC)) * framesPerSquare 

	for frame in range(frameCount + 1):
		r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
		drawBoard(screen)
		drawPieces(screen, board)
		color = colors[(move.endRow + move.endCol) % 2]
		endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
		pg.draw.rect(screen, color, endSquare)

		if move.pieceCaptured != "--":
			screen.blit(IMAGES[move.pieceCaptured], endSquare)
		screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
		pg.display.flip()

		if abs(dR) + abs(dC) > 5:
			clock.tick(180)
		elif dR+dC > 2:
			clock.tick(120)
		else:
			clock.tick(80)

def drawText(screen, text):
	font = pg.font.SysFont('Helvetica', 32, True, False)
	textObject = font.render(text, 0, pg.Color('black'))
	textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
	screen.blit(textObject, textLocation)

if __name__ == "__main__":
	main()  