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
        self.fallSpeed = 20
        self.timeToDrop = self.fallSpeed

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
        
        #gallery.renderBackground(gfx)
        gfx.blit(gallery.background, (0, 0))
        self.stats.render(gfx)
        
        # Render grid blocks
        for x in range(GridSize.width):
            for y in range(GridSize.height):
                if self.grid[x][y]:
                    gallery.renderBlock(gfx, self.stats.level, self.grid[x][y] - 1, Point(x, y))

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
            if self.currPiece.pos.y <= 0:
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
        self.newPiece()        
    
    # Shift above rows down from cleared row.
    def shiftRowDown(self, row):
        for x in range(GridSize.width):
            for y in reversed(range(row)):
                self.grid[x][y + 1] = self.grid[x][y]
                self.grid[x][y] = 0

    # Set piece values into grid.                
    def setGridPiece(self, piece):
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):
                if piece.grid[y][x]:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = piece.grid[y][x]
    
    # Remove piece values from grid.
    def clearGridPiece(self, piece):
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):
                if piece.grid[y][x]:
                    self.grid[piece.pos.x + x][piece.pos.y + y] = 0
    
    # Check if piece can be moved to new location
    def validMove(self, piece):
        
        for y in range(len(piece.grid)):
            for x in range(len(piece.grid[y])):

                if piece.grid[y][x]:
                    if piece.pos.x + x < 0 or piece.pos.x + x >= GridSize.width:
                        return False
                    if piece.pos.y + y < 0 or piece.pos.y + y >= GridSize.height:
                        return False
                    if self.grid[piece.pos.x + x][piece.pos.y + y]:
                        return False
                
        return True
    
    # Create new piece.
    def newPiece(self):
        self.currPiece = randomPiece()
        self.setGridPiece(self.currPiece)
    
    # Start a new game.
    def newGame(self):
        self.grid = [[0 for y in range(GridSize.height)] for x in range(GridSize.width)]
        self.stats = Statistics()
        self.newPiece()
        self.mixer.play(Sound.Start)
        self.mixer.loopMusic()
        
    # End the game
    def endGame(self):
        self.mixer.play(Sound.GameOver)
        self.currPiece = None
        
    # Return if game is over
    def gameOver(self):
        if not self.currPiece:
            return True
        else:
            return False

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