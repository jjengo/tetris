# Author: Jonathan Jengo

from random import randint
from .util import Point, Dimension
  
# Create a random piece
def randomPiece():
    
    rand = randint(0, 6)
    piece = None
    
    if rand == 0:
        piece = SquarePiece()
        piece.pos.set(3, -1)
    elif rand == 1:
        piece = IPiece()
        piece.pos.set(3, -2)
    elif rand == 2:
        piece = JPiece()
        piece.pos.set(3, -1)
    elif rand == 3:
        piece = LPiece()
        piece.pos.set(2, -1)
    elif rand == 4:
        piece = TPiece()
        piece.pos.set(2, -2)
    elif rand == 5:
        piece = SPiece()
        piece.pos.set(2, -1)
    elif rand == 6:
        piece = ZPiece()
        piece.pos.set(2, -1)
    
    return piece
    
# A 4x4 matrix representing a grid piece
class Piece:
    
    # Initialize
    def __init__(self):
        self.grid = []
        self.pos = Point(0, 0)
        self.origin = Point(0, 0)
        self.size = Dimension(0, 0)
    
    # Set the grid values.
    def set(self, grid):
        self.grid = grid
        self.origin = Point(self.left(), self.top())
    
    # Rotate piece grid counter clockwise
    def rotateLeft(self):
        rotated = zip(*self.grid)[::-1]
        self.set(rotated)
        self.size = self.size.rotate()
        
    # Rotate piece grid clockwise
    def rotateRight(self):
        rotated = zip(*self.grid[::-1])
        self.set(rotated)
        self.size = self.size.rotate()

    # Return the first non-empty row
    def top(self):
        for y in range(len(self.grid)):
            if len([x for x in range(len(self.grid[y])) if self.grid[y][x]]):
                return y
        return 0
    
    # Return the first non-empty column
    def left(self):
        left = 5
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] and x < left:
                    left = x
        return left

# Square shaped piece.
class SquarePiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.size.set(2, 2)
        self.set([[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]])

# Long shaped piece.
class IPiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.size.set(4, 1)
        self.set([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [1, 1, 1, 1],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]])
    
# J shaped piece.
class JPiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.size.set(3, 2)
        self.set([[0, 0, 0, 0],
                  [2, 2, 2, 0],
                  [0, 0, 2, 0],
                  [0, 0, 0, 0]])
        
# L shaped piece
class LPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.size.set(3, 2)
        self.set([[0, 0, 0, 0],
                  [0, 2, 2, 2],
                  [0, 2, 0, 0],
                  [0 ,0, 0, 0]])
        
# T shaped piece.
class TPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.size.set(3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 0],
                  [0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0]])
        
# S shaped piece.
class SPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.size.set(3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 0, 3, 3, 0],
                  [0, 3, 3, 0, 0],
                  [0, 0, 0, 0, 0]])
                
# Z shaped piece.
class ZPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.size.set(3, 2)
        self.set([[0, 0, 0, 0, 0],
                  [0, 3, 3, 0, 0],
                  [0, 0, 3, 3, 0],
                  [0, 0, 0, 0, 0]])
        
        