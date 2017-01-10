#!/usr/bin/python

import sys
import random

class Board:
    def __init__(self, w, h, p1, p2):
	self.rows = h
        self.cols = w
        self.board = [['-' for x in range(w)] for y in range(h)]
        self.colPos = [h for x in range(w)]
	self.result = "IN_PROGRESS"
	self.seqP1 = [p1] * 4
	self.seqP2 = [p2] * 4
	self.lastC = -1
	self.lastR = -1

    def printBoard(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.lastC == c and self.lastR == r:
                   print "*%s|" % '{:^7.7}'.format(self.board[r][c]),
		else:
                   print "%s|" % '{:^8.8}'.format(self.board[r][c]),
	    print ""
        for i in range(5 * self.cols):
            print "-",
        print ""
        for i in range(self.cols):
            print "%s " % '{:^8}'.format(i),
        print "" 

    def remove(self, col):
        if col < 0 or col >= self.cols:
	   print "Enter a number between 0 and %d to remove" %  (self.cols - 1)
        
	if self.colPos[col] == self.rows:
           print "Column is empty. Try another column" 

	self.board[self.colPos[col]][col] = '-'
	self.colPos[col] = self.colPos[col] + 1

    def add(self, player, col, showError=True, markLastPlaced=True):
	if col < 0 or col >= self.cols:
	   print "Enter a number between 0 and %d" %  (self.cols - 1)
	   return False
	if (self.colPos[col] == 0):
           if showError:
              print "Column is full. Try another column" 
           return False
	self.colPos[col] = self.colPos[col] - 1
	self.board[self.colPos[col]][col] = player
	if markLastPlaced:
	   self.lastC = col
	   self.lastR = self.colPos[col]
        return True

    def getEndingRow(self, r, c):
	start = c - 3
        if start < 0:
           start = 0
        return self.board[r][start:c+1]

    def getEndingCol(self, r, c):
	start = r - 3
        if r-3 < 0:
           start = 0
        return [row[c] for row in self.board[start:r+1]]

    def getEndingLDiag(self, r, c):
        seq = []
	for i in range(4):
	    if r-i >= 0 and c-i >= 0:
               seq.append(self.board[r-i][c-i])
	return seq

    def getEndingRDiag(self, r, c):
	seq = []
        for i in range(4):
	    if r-i >= 0 and c+i < self.cols:
	       seq.append(self.board[r-i][c+i])
	return seq

    def gameOver(self):
        numEmpty = 0
	for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '-':
		   numEmpty = numEmpty + 1
                   next
		seq = self.getEndingRow(r,c)
		if seq == self.seqP1 or seq == self.seqP2:
                   return True
		seq = self.getEndingCol(r,c)
		if seq == self.seqP1 or seq == self.seqP2:
                   return True
		seq = self.getEndingLDiag(r,c)
		if seq == self.seqP1 or seq == self.seqP2:
                   return True
		seq = self.getEndingRDiag(r,c)
		if seq == self.seqP1 or seq == self.seqP2:
                   return True
	if numEmpty == 0:
	   self.result = "DRAW"
	   return True
	return False
    

class Player:
    def __init__(self, name, opponent, board):
        self.name = name
	self.opponent = opponent
        self.board = board
	self.moves = []
    
class RandomPlayer(Player):
    def move(self):
	move = random.randrange(self.board.cols)
        while not self.board.add(curPlayer, move, False): 
	      move = random.randrange(self.board.cols)
	self.moves.append(move)

class SmartPlayer(Player):
    def getWinningCols(self, player):
        cols = []
        for c in range(self.board.cols):
            if self.board.add(player,c, False, False):
               if self.board.gameOver():
                  self.board.remove(c)
                  cols.append(c)
               else:
                  self.board.remove(c)
        return cols

    def findAtleastOneMove(self):
	for c1 in range(self.board.cols):
            if self.board.add(self.opponent, c1, False, False):
               foundMove = False
               for c2 in range(self.board.cols):
                   if self.board.add(self.name, c2, False, False):
		      if len(self.getWinningCols(self.opponent)) < 1:
	                 self.board.remove(c2)
			 foundMove = True
			 break
	              self.board.remove(c2)
	       if not foundMove:
		  self.board.remove(c1)
		  return False
	       self.board.remove(c1)
	return True

    def getSeqScore(self, seq):
	score = 0
	for e in seq:
	    if e == self.name:
	       score = score + 1
	    elif e == self.opponent:
	       score = score + 4
	    else:
		score = score + 2
	return score
	
    def getCellScore(self,c):
	r = min(self.board.rows-1,self.board.colPos[c])
	r = max(0,r)
	score = self.getSeqScore(self.board.getEndingRow(r,c))
	score = score + self.getSeqScore(self.board.getEndingCol(r,c))
	score = score + self.getSeqScore(self.board.getEndingLDiag(r,c))
	score = score + self.getSeqScore(self.board.getEndingRDiag(r,c))
	return score 

    def randomMove(self, moves):
	move = random.choice(moves)
        while not self.board.add(curPlayer, move, False): 
	      move = random.choice(moves)
	self.moves.append(move)

    def move(self):
        # can he or i win now?
        # if so, block or win
	c = self.getWinningCols(self.name) 
        if len(c) == 0:
           c = self.getWinningCols(self.opponent)
        if len(c) > 0:
           self.board.add(self.name, c[0])
	   self.moves.append(c[0])
	   #print "Moves0:",c	
           return

	# can he win in the next move?
        # collect all good moves 
        moves1 = []
	for c1 in range(self.board.cols):
	    if self.board.add(self.name, c1, False, False):
               if len(self.getWinningCols(self.opponent)) == 0:
                  moves1.append(c1)
               self.board.remove(c1)
 	if len(moves1) == 0:
           print "Computer couldn't find a good move" 
           return self.randomMove([x for x in range(self.board.cols)])
        else:
	   for c in moves1:
               if self.board.add(self.name, c, False):
                  if len(self.getWinningCols(self.name)) > 1:
		     self.moves.append(c)
		     return
		  self.board.remove(c)
	
	#print "Moves1: ", moves1
	moves2 = []
	for c1 in moves1:
	    if self.board.add(self.name, c1, False, False):
               goodMove = True
	       for c2 in range(self.board.cols): 
		   if self.board.add(self.opponent, c2, False, False):
		      if len(self.getWinningCols(self.opponent)) > 1:
                         goodMove = False
                         self.board.remove(c2)
                         break 
                      self.board.remove(c2)
               if goodMove:
		  moves2.append(c1)
               self.board.remove(c1)
                      
        if len(moves2) == 0:
           print "Computer couldn't find a good move2" 
           return self.randomMove(moves1)

	#print "Moves2: ", moves2

	moves3 = []
        for c1 in moves2:
	    if self.board.add(self.name, c1, False, False):
	       if self.findAtleastOneMove():
		  moves3.append(c1)
               self.board.remove(c1)
                 
        if len(moves3) == 0:
           print "Computer couldn't find a good move3" 
           return self.randomMove(moves2)

	#print "Moves3: ", moves3

	scores = []
	bestScore = -100000
	for c in moves3:
            score = self.getCellScore(c)
	    if score > bestScore:
               bestScore = score 
	       bestMove = c
        
        if self.board.add(self.name, bestMove, False):
	   self.moves.append(bestMove)
	   return
	else:
           return self.randomMove(moves3)
	   
class HumanPlayer(Player):
    def move(self):
	col =  input("Enter move: ")
        while not self.board.add(curPlayer, col): 
            col =  input("Enter move: ")
	self.moves.append(col)
        return 

        
if (len(sys.argv) < 3):
   print "Usage: %s <p1Name> <p2Name>" % sys.argv[0]
   print "If playername contains 'comp' the program moves smartly for that player"
   print "If playername contains 'rand' the program moves randomly for that player"

   sys.exit(0)

p1Name = sys.argv[1]
p2Name = sys.argv[2]

print "Game : (%s) vs (%s)\n" %  (p1Name, p2Name )

b = Board(7, 6, p1Name, p2Name)
curPlayer = p1Name

if 'Comp' in p1Name or 'comp' in p1Name:
   p1 = SmartPlayer(p1Name, p2Name, b)
elif 'Rand' in p1Name or 'rand' in p1Name:
   p1 = RandomPlayer(p1Name, p2Name, b)
else:
   p1 = HumanPlayer(p1Name, p2Name, b)

if 'Comp' in p2Name or 'comp' in p2Name:
   p2 = SmartPlayer(p2Name, p1Name, b)
elif 'Rand' in p2Name or 'rand' in p2Name:
   p2 = RandomPlayer(p2Name, p1Name, b)
else:
   p2 = HumanPlayer(p2Name, p1Name, b)

while (b.gameOver() == False):
      if curPlayer == p2Name:
	 p2.move()
         curPlayer = p1Name
      else:
	 p1.move()
         curPlayer = p2Name
	 
      b.printBoard()

if b.result == "DRAW":
   print "Game Over: DRAW!!"
else:
   if curPlayer == p1Name:
      curPlayer = p2Name
   else:
      curPlayer = p1Name
   print "Game Over: Player %s won!!!" % curPlayer 

print p1.name,p1.moves
print p2.name,p2.moves
   

