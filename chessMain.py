import pygame as pg
import pygame_menu
from multiprocessing import Process, Queue
from ctypes import windll
from chessGame import start_the_game, surface

SetWindowPos = windll.user32.SetWindowPos
pg.init()
x, y = 100, 100
SetWindowPos(pg.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)
playerOneVALUE = True
playerTwoVALUE = False

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
menu.add.button('Play', lambda:start_the_game(playerOneVALUE, playerTwoVALUE))
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.label(HELP, max_char=-1, font_size=16)
 