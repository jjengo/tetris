# Author: Jonathan Jengo

import sys
import pygame
from pygame.locals import *

from .image import Gallery
from .util import Point, Dimension
from .sound import Sound, Mixer
from .piece import Piece, randomPiece

# Size of the grid matrix.
GridSize = Dimension(10, 20)

# Tetris game engine
class Tetris:

    # Initialize
    def __init__(self):
        self.grid = []
        self.mixer = Mixer()
        self.stats = Statistics()
        self.currPiece = randomPiece()
        self.nextPiece = randomPiece()
        self.fallSpeed = 28
        self.timeToDrop = self.fallSpeed
        self.running = False

    # Process key state events.
    def processKeyEvents(self, keys):

        if K_LEFT in keys:
            self.lateralPieceMove(-1)
        elif K_RIGHT in keys:
            self.lateralPieceMove(1)
        elif K_DOWN in keys:
            self.dropPiece()
        elif K_UP in keys:
            self.rotatePiece(1)
            
    # Update all states.
    def update(self):
        
        # Countdown to current piece drop
        self.timeToDrop -= 1
        if self.timeToDrop < 0:
            self.timeToDrop = self.fallSpeed
            self.descendPiece()
        
    # Render all sprites.
    def render(self, gfx, gallery):
        
        gfx.blit(gallery.background, (0, 0))
        self.stats.render(gfx)
        
        # Render grid blocks
        for x in range(GridSize.width):
            for y in range(GridSize.height):
                if self.grid[x][y] > 0:
                    gallery.renderBlock(gfx, self.stats.level, self.grid[x][y] - 1, Point(x, y))
                elif self.grid[x][y] < 0:
                    gallery.renderGhost(gfx, (self.grid[x][y] * -1) - 1, Point(x, y))

        # Render next blocks
        for y in range(len(self.nextPiece.grid)):
            for x in range(len(self.nextPiece.grid[y])):
                if self.nextPiece.grid[y][x]:
                    pt = Point(x - self.nextPiece.origin.x, y - self.nextPiece.origin.y)
                    gallery.renderNext(gfx, self.stats.level, self.nextPiece.grid[y][x] - 1, self.nextPiece.size, pt)

    # Translate piece by delta
    def lateralPieceMove(self, dx):
        
        self.clearGridPiece(self.currPiece)
        
        self.currPiece.pos.x += dx
        if not self.validMove(self.currPiece):
            self.currPiece.pos.x -= dx
        else:
            self.mixer.play(Sound.Lateral)
            
        self.setGridPiece(self.currPiece)
    
    # Rotate piece by delta
    def rotatePiece(self, dr):
        
        self.clearGridPiece(self.currPiece)
        
        if dr < 0:
            self.currPiece.rotateLeft()
            if not self.validMove(self.currPiece):
                self.currPiece.rotateRight()
            else:
                self.mixer.play(Sound.Rotate)
        elif dr > 0:
            self.currPiece.rotateRight()
            if not self.validMove(self.currPiece):
                self.currPiece.rotateLeft()
            else:
                self.mixer.play(Sound.Rotate)
                
        self.setGridPiece(self.currPiece)
    
    # Descent piece by a single row
    def descendPiece(self):
        self.dropPiece(1)
    
    # Drop piece to the bottom
    def dropPiece(self, incr=GridSize.height):
        
        self.clearGridPiece(self.currPiece)
        
        # Find grid bottom
        place = False
        for i in range(incr):
            self.currPiece.pos.y += 1
            if not self.validMove(self.currPiece):
                self.currPiece.pos.y -= 1
                place = True
                break
        
        self.setGridPiece(self.currPiece)
        if place:
            if self.currPiece.pos.y + self.currPiece.origin.x <= 0:
                self.endGame()
            else:
                self.placePiece(self.currPiece)

    # Place piece at grid bottom
    def placePiece(self, piece):
        
        # Find cleared rows
        cleared = []
        for y in range(GridSize.height):
            if (len([x for x in range(GridSize.width) if self.grid[x][y]]) == GridSize.width):
                cleared.append(y)
                
        # Clear rows & shift down remains.
        if cleared:
            for row in cleared:
                for x in range(GridSize.width):
                    self.grid[x][row] = 0
            for row in cleared:
                self.shiftRowDown(row)
            
        # Update statistics.
        self.mixer.playDropped(len(cleared))
        if self.stats.update(len(cleared)):
            self.mixer.play(Sound.LevelUp)
            if self.fallSpeed > 5:
                self.fallSpeed -= 2
            
        self.newPiece()        
    
    # Shift above rows down from cleared row.
    def shiftRowDown(self, row):
        for x in range(GridSize.width):
            for y in reversed(range(row)):
                self.grid[x][y + 1] = self.grid[x][y]
                self.grid[x][y] = 0

    # Set piece values into grid.                
    def setGridPiece(self, piece):
        
        # Find and set piece ghost grid points
        yorig = piece.pos.y
        for y in range(GridSize.height - piece.pos.y):
            piece.pos.y += 1
            if not self.validMove(piece):
                piece.pos.y -= 1
                break
        
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):
                if piece.grid[y][x]:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = (piece.grid[y][x] * -1)
        
        # Set grid values for piece.
        piece.pos.y = yorig
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):
                if piece.grid[y][x] and piece.pos.y + y >= 0:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = piece.grid[y][x]
    
    # Remove piece values from grid.
    def clearGridPiece(self, piece):
        
        # Clear ghost grid points.
        for x in range(GridSize.width):
            for y in range(GridSize.height):
                if self.grid[x][y] < 0:
                    self.grid[x][y] = 0
        
        # Clear piece grid points.
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):
                if piece.grid[y][x] and piece.pos.y + y >= 0:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = 0
    
    # Check if piece can be moved to new location
    def validMove(self, piece):
        
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):

                pt = Point(piece.pos.x + x, piece.pos.y + y)
                if piece.grid[y][x] and pt.y >= 0:
                    if pt.x < 0 or pt.x >= GridSize.width or pt.y >= GridSize.height:
                        return False
                    if self.grid[pt.x][pt.y]:
                        return False
        return True
    
    # Create new piece.
    def newPiece(self):
        self.currPiece = self.nextPiece
        self.nextPiece = randomPiece()
        if not self.validMove(self.currPiece):
            self.endGame()
        self.setGridPiece(self.currPiece)
    
    # Start a new game.
    def newGame(self):
        self.grid = [[0 for y in range(GridSize.height)] for x in range(GridSize.width)]
        self.stats = Statistics()
        self.newPiece()
        self.mixer.play(Sound.Start)
        self.mixer.loopMusic()
        self.running = True
        
    # End the game
    def endGame(self):
        self.mixer.play(Sound.GameOver)
        self.running = False
        
    # Return if game is over
    def gameOver(self):
        return not self.running

# Game statistics
class Statistics:
    
    Scores = {0:10, 1:100, 2:300, 3:500, 4:1000}
    
    # Initialize
    def __init__(self):
        self.score = 0
        self.level = 0
        self.lines = 0
        
    # Render statistics values
    def render(self, gfx):

        font = pygame.font.SysFont("OCR A Extended", 14, True)
        label = font.render("LEVEL", 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 190))
        label = font.render("LINES", 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 260))
        
        font = pygame.font.SysFont("OCR A Extended", 28)
        label = font.render(repr(self.score), 1, (255, 255, 255))
        gfx.blit(label, (340 - label.get_width(), 5))
        label = font.render(repr(self.level), 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 207))
        label = font.render(repr(self.lines), 1, (255, 255, 255))
        gfx.blit(label, (70 - (label.get_width() / 2), 277))

    # Update stats based on # cleared lines
    def update(self, cleared):
        self.score += Statistics.Scores[cleared]
        self.lines += cleared
        if self.lines / 10 > self.level:
            self.level += 1
            return True
        else:
            return False