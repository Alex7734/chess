class GameState():

	def __init__(self):
		self.board = [
			["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
			["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
			["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
		]
		self.whiteToMove = True
		self.moveLog = []
		self.wKLocation = (7, 4)
		self.bKLocation = (0, 4)
		self.checkMate = False
		self.staleMate = False
		self.enpassantPossible = ()
		self.currentCastlingRights = CastleRights(True, True, True, True)
		self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
								self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove

		if  move.pieceMoved == "wK":
			self.wKLocation = (move.endRow, move.endCol)
		elif move.pieceMoved == "bK":
			self.bKLocation = (move.endRow, move.endCol)

		# make a menu to chose from only in main not in makeMove as this is used by the engine too
		# in order to make it simple for now it's auto queen on and I will consider it a feature not a bug
		if move.isPawnPromotion:
			self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

		if move.isEnpassantMove:
			self.board[move.startRow][move.endCol] = '--'

		if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
			self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
		else:
			self.enpassantPossible = ()

		if move.isCastleMove:
			if move.endCol - move.startCol == 2:
				self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
				self.board[move.endRow][move.endCol+1] = "--"
			else:
				self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
				self.board[move.endRow][move.endCol-2] = "--"

		self.updateCastleRights(move)
		self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
									self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


	def updateCastleRights(self, move):
		if move.pieceMoved == "wK":
			self.currentCastlingRights.wks = False
			self.currentCastlingRights.wqs = False
		if move.pieceMoved == "bK":
			self.currentCastlingRights.bks = False
			self.currentCastlingRights.bqs = False
		if move.pieceMoved == "wR":
			if move.startRow == 7:
				if move.startCol == 0:
					self.currentCastlingRights.wqs = False
				elif move.startCol == 7:
					self.currentCastlingRights.wks = False
		if move.pieceMoved == "bR":
			if move.startRow == 0:
				if move.startCol == 0:
					self.currentCastlingRights.bqs = False
				elif move.startCol == 7:
					self.currentCastlingRights.bks = False
		if move.pieceCaptured == 'wR':
			if move.endRow == 7:
				if move.endCol == 0:
					self.currentCastlingRights.wqs = False
				elif move.endCol == 7:
					self.currentCastlingRights.wks = False
		elif move.pieceCaptured == 'bR':
			if move.endRow == 0:
				if move.endCol == 0:
					self.currentCastlingRights.bqs = False
				elif move.endCol == 7:
					self.currentCastlingRights.bks = False

	def undoMove(self):
		if len(self.moveLog) != 0:
			lastMove = self.moveLog.pop()
			self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
			self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
			self.whiteToMove = not self.whiteToMove

			if  lastMove.pieceMoved == "wK":
				self.wKLocation = (lastMove.startRow, lastMove.startCol)
			elif lastMove.pieceMoved == "bK":
				self.bKLocation = (lastMove.startRow, lastMove.startCol)

			if lastMove.isEnpassantMove:
				self.board[lastMove.endRow][lastMove.endCol] = "--"
				self.board[lastMove.startRow][lastMove.endCol] = lastMove.pieceCaptured
				self.enpassantPossible = (lastMove.endRow, lastMove.endCol)

			if lastMove.pieceMoved[1] == 'P' and abs(lastMove.startRow - lastMove.endRow) == 2:
				self.enpassantPossible = ()

			self.castleRightsLog.pop()
			newRights = self.castleRightsLog[-1]
			self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

			if lastMove.isCastleMove:
				if lastMove.endCol - lastMove.startCol == 2:
					self.board[lastMove.endRow][lastMove.endCol+1] = self.board[lastMove.endRow][lastMove.endCol-1]
					self.board[lastMove.endRow][lastMove.endCol-1] = "--"
				else:
					self.board[lastMove.endRow][lastMove.endCol-2] = self.board[lastMove.endRow][lastMove.endCol+1]
					self.board[lastMove.endRow][lastMove.endCol+1] = "--"

			self.checkMate = False
			self.staleMate = False

	def getValidMoves(self):
		tempEnpassantPosible = self.enpassantPossible
		tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
										self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
		moves = self.getAllPossibleMoves()

		if self.whiteToMove:
			self.getCastleMoves(self.wKLocation[0], self.wKLocation[1], moves)
		else:
			self.getCastleMoves(self.bKLocation[0], self.bKLocation[1], moves)

		for i in range(len(moves)-1, -1, -1):
			self.makeMove(moves[i])
			self.whiteToMove = not self.whiteToMove
			if self.inCheck():
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove
			self.undoMove()
		if len(moves) == 0:
			if self.inCheck():
				self.checkMate = True
			self.staleMate = False
		else:
			self.checkMate = False
			self.staleMate = False

		self.enpassantPossible = tempEnpassantPosible
		self.currentCastlingRights = tempCastleRights
		return moves 

	def inCheck(self):
		if self.whiteToMove:
			return self.squareUnderAttack(self.wKLocation[0], self.wKLocation[1])
		else:
			return self.squareUnderAttack(self.bKLocation[0], self.bKLocation[1])

	def squareUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove
		oppMoves = self.getAllPossibleMoves()
		self.whiteToMove = not self.whiteToMove
		for move in oppMoves:
			if move.endRow == r and move.endCol == c:
				return True
		return False

	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
					piece = self.board[r][c][1]
					if piece == 'P':
						self.getPawnMoves(r, c, moves)
					elif piece == "R":
						self.getRookMoves(r, c, moves)
					elif piece == "B":
						self.getBishopMoves(r, c, moves)
					elif piece == "N":
						self.getKnightMoves(r, c, moves)
					elif piece == "Q":
						self.getQueenMoves(r, c, moves)
					elif piece == "K":
						self.getKingMoves(r, c, moves)
		return moves

	def getPawnMoves(self, r, c, moves):
		if self.whiteToMove:
			if self.board[r-1][c] == "--":
				moves.append(Move((r,c), (r-1,c), self.board))
				if r == 6 and self.board[r-2][c] == "--":
					moves.append(Move((r,c), (r-2,c), self.board))
			if c-1 >= 0:
				if self.board[r-1][c-1][0] == "b":
					moves.append(Move((r,c), (r-1,c-1), self.board))
				elif (r-1, c-1) == self.enpassantPossible:
					moves.append(Move((r,c), (r-1,c-1), self.board, isEnpassantMove=True))

			if c+1 <= 7:
				if self.board[r-1][c+1][0] == "b":
					moves.append(Move((r,c), (r-1,c+1), self.board))
				elif (r-1, c+1) == self.enpassantPossible:
					moves.append(Move((r,c), (r-1,c+1), self.board, isEnpassantMove=True))
		else:
			if self.board[r+1][c] == "--":
				moves.append(Move((r,c), (r+1,c), self.board))
				if r == 1 and self.board[r+2][c] == "--":
				 	moves.append(Move((r,c), (r+2,c), self.board))
			if c-1 >= 0:
				if self.board[r+1][c-1][0] == "w":
					moves.append(Move((r,c), (r+1,c-1), self.board))
				elif (r+1, c-1) == self.enpassantPossible:
					moves.append(Move((r,c), (r+1,c-1), self.board, isEnpassantMove=True))
			if c+1 <= 7:
				if self.board[r+1][c+1][0] == "w":
					moves.append(Move((r,c), (r+1,c+1), self.board))
				elif (r+1, c+1) == self.enpassantPossible:
					moves.append(Move((r,c), (r+1,c+1), self.board, isEnpassantMove=True))
	

	def getRookMoves(self, r, c, moves):
		directions = ((-1, 0), (0, -1), (1, 0), (0,1))
		enemyColor = "b" if self.whiteToMove else "w"
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: 
					endPiece = self.board[endRow][endCol]
					if endPiece == "--":
						moves.append(Move((r,c), (endRow,endCol), self.board))
					elif endPiece[0] == enemyColor:
						moves.append(Move((r,c), (endRow, endCol), self.board))
						break
					else:
						break
				else:
					break

	def getBishopMoves(self, r, c, moves):
		directions = ((-1, -1), (-1, 1), (1, -1), (1,1))
		enemyColor = "b" if self.whiteToMove else "w"
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: 
					endPiece = self.board[endRow][endCol]
					if endPiece == "--":
						moves.append(Move((r,c), (endRow,endCol), self.board))
					elif endPiece[0] == enemyColor:
						moves.append(Move((r,c), (endRow, endCol), self.board))
						break
					else:
						break
				else:
					break

	def getKnightMoves(self, r, c, moves):
		knightMoves = ((-2, -1),(-2, 1),(2, -1),(2, 1),(-1, -2),(-1, 2),(1, -2),(1, 2))
		allyColor = "w" if self.whiteToMove else "b"
		for m in knightMoves:
			endRow = r + m[0]
			endCol = c + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor:
					moves.append(Move((r,c), (endRow,endCol), self.board))

	def getQueenMoves(self, r, c, moves):
		self.getRookMoves(r, c, moves)
		self.getBishopMoves(r, c, moves)

	def getKingMoves(self, r, c, moves):
		kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		allyColor = "w" if self.whiteToMove else "b"
		for i in range(8):
			endRow = r + kingMoves[i][0]
			endCol = c + kingMoves[i][1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor:
					moves.append(Move((r,c), (endRow,endCol), self.board))
	
	def getCastleMoves(self, r, c, moves):
		if self.squareUnderAttack(r,c):
			return
		if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
			self.getKingsideCastleMoves(r, c, moves)
		if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
			self.getQueensideCastleMoves(r, c, moves)


	def getKingsideCastleMoves(self, r, c, moves):
		if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
			if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
				moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True)) 

	def getQueensideCastleMoves(self, r, c, moves):
		if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
			if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
				moves.append(Move((r,c), (r, c-2), self.board, isCastleMove=True)) 

class Move():

	ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[int(self.startRow)][int(self.startCol)]
		self.pieceCaptured = board[int(self.endRow)][int(self.endCol)]
		self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
		self.isPawnPromotion = False
		self.isEnpassantMove = isEnpassantMove

		if self.isEnpassantMove:
			self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
		if (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7):
			self.isPawnPromotion = True

		self.isCastleMove = isCastleMove

	def getChessNotation(self):
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)		

	def getRankFile(self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]

	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID
		return False

class CastleRights():
	def __init__(self, wks, bks, wqs, bqs):
		self.wks = wks
		self.bks = bks
		self.wqs = wqs
		self.bqs = bqs