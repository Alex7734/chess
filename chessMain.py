import pygame as pg
import chessEngine as cE
import mihocFish as AI
import pygame_menu
from multiprocessing import Process, Queue
from ctypes import windll

SetWindowPos = windll.user32.SetWindowPos

pg.init()
WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}
surface = pg.display.set_mode((WIDTH, HEIGHT))
playerOneVALUE = True
playerTwoVALUE = False

x, y = 100, 100
SetWindowPos(pg.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)

def playWith(value, v):
	global playerOneVALUE, playerTwoVALUE
	if v == 1:
		playerOneVALUE = True
		playerTwoVALUE = False
	elif v == 2:
		playerOneVALUE = False
		playerTwoVALUE = True
	elif v == 3:
		playerOneVALUE = False
		playerTwoVALUE = False
	elif v == 4:
		playerOneVALUE = True
		playerTwoVALUE = True

def loadImages():
	pieces = ['wP', 'wR', 'wB', 'wN', 'wQ', 'wK', 'bP', 'bR', 'bB', 'bN', 'bK', 'bQ']
	for piece in pieces:
		IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def start_the_game():
	clock = pg.time.Clock()
	surface.fill(pg.Color("white"))
	gs = cE.GameState()
	loadImages()
	running = True
	sqSelected = ()
	playerClicks = []
	validMoves = gs.getValidMoves()
	moveMade = False
	animate = False
	gameOver = False
	playerOne = playerOneVALUE 
	playerTwo = playerTwoVALUE
	AIThinking = False
	moveFinderProcess = None
	moveUndone = False

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
					if AIThinking:
						moveFinderProcess.terminate()
						AIThinking = False
					moveUndone = True
				if e.key == pg.K_r:
					gs = cE.GameState()
					validMoves = gs.getValidMoves()
					sqSelected = ()
					playerClicks = []
					moveMade = False
					animate = False
					gameOver = False
					if AIThinking:
						moveFinderProcess.terminate()
						AIThinking = False
					moveUndone = True
				if e.key == pg.K_q:
					menu.mainloop(surface)

		# AI decision
		if not gameOver and not humanTurn and not moveUndone:
			if not AIThinking:
				AIThinking = True
				print('thinking...')
				pg.event.post(pg.event.Event(7734))
				returnQueue = Queue() # used to pass data between threads
				moveFinderProcess = Process(target=AI.findBestMoveNegaMax, args=(gs, validMoves, returnQueue))
				moveFinderProcess.start()

			if not moveFinderProcess.is_alive():
				print("done thinking")
				AIMove = returnQueue.get()
				if AIMove is None:
					AIMove = AI.findRandomMove(validMoves)
				gs.makeMove(AIMove)
				moveMade = True
				animate = True
				AIThinking = False

		# Human decision
		if moveMade:
			if animate:
				animateMove(gs.moveLog[-1], surface, gs.board, clock)
			validMoves= gs.getValidMoves()
			moveMade = False
			animate = False
			moveUndone = False

		drawGameState(surface, gs, validMoves, sqSelected)

		# Check end of game
		if gs.checkMate:
			gameOver = True
			if gs.whiteToMove:
				drawText(surface, 'Black wins by checkmate!')
			else:
				drawText(surface, 'White wins by checkmate!')
		elif gs.staleMate:
			gameOver = True
			drawText(surface, 'Stalemate')

		clock.tick(MAX_FPS)
		pg.display.flip()

def drawGameState(surface, gs, validMoves, sqSelected):
	drawBoard(surface)
	highlightSquares(surface, gs, validMoves, sqSelected)
	drawPieces(surface, gs.board)

def highlightSquares(surface, gs, validMoves, sqSelected):
	if sqSelected != ():
		r, c = sqSelected
		if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
			s = pg.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(100)
			s.fill(pg.Color('blue'))
			surface.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
			s.fill(pg.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					surface.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawBoard(surface):
	colors = [(235, 235, 208), (119, 148, 85)]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c)%2)]
			pg.draw.rect(surface, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(surface, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != "--":
				surface.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, surface, board, clock):

	colors = [(235, 235, 208), (119, 148, 85)]	
	cords = []
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framesPerSquare = 10 
	frameCount = (abs(dR) + abs(dC)) * framesPerSquare 

	for frame in range(frameCount + 1):
		r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
		drawBoard(surface)
		drawPieces(surface, board)
		color = colors[(move.endRow + move.endCol) % 2]
		endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
		pg.draw.rect(surface, color, endSquare)

		if move.pieceCaptured != "--":
			surface.blit(IMAGES[move.pieceCaptured], endSquare)
		surface.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
		pg.display.flip()

		if abs(dR) + abs(dC) > 5:
			clock.tick(180)
		elif dR+dC > 2:
			clock.tick(120)
		else:
			clock.tick(80)

def drawText(surface, text):
	font = pg.font.SysFont('Helvetica', 32, True, False)
	textObject = font.render(text, 0, pg.Color('black'))
	textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
	surface.blit(textObject, textLocation)

menu = pygame_menu.Menu('Mihoc Fish', 512, 512,
                       theme=pygame_menu.themes.THEME_DEFAULT)

HELP = f'''
	  INSTRUCTIONS
Press q to go back to menu 
Press r to reset the game 
Press z to undo the move 
Press RMB to move pieces 
''' 

menu.add.selector('', [('Play with white', 1), ('Play with black', 2), ('Let computers play', 3), ('Two player mode', 4)], onchange=playWith)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.label(HELP, max_char=-1, font_size=16)

if __name__ == "__main__":
	menu.mainloop(surface)
 