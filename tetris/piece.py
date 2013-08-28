# Author: Jonathan Jengo

from random import randint
from .util import Point, Dimension
  
# Create a random piece
def randomPiece():
    
    rand = randint(0, 6)
    if rand == 0:
        return SquarePiece()
    elif rand == 1:
        return IPiece()
    elif rand == 2:
        return JPiece()
    elif rand == 3:
        return LPiece()
    elif rand == 4:
        return TPiece()
    elif rand == 5:
        return SPiece()
    elif rand == 6:
        return ZPiece()
    else:
        return None

# A 4x4 matrix representing a grid piece
class Piece:
    
    # Initialize
    def __init__(self):
        self.grid = []
        self.pos = Point(0, 0)
    
    # Rotate piece grid counter clockwise
    def rotateLeft(self):
        rotated = zip(*self.grid)[::-1]
        self.grid = rotated
    
    # Rotate piece grid clockwise
    def rotateRight(self):
        rotated = zip(*self.grid[::-1])
        self.grid = rotated
        
    # Return the first non-empty row
    def top(self):
        for y in range(len(self.grid)):
            if len([x for x in range(len(self.grid[y])) if self.grid[y][x]]):
                return self.pos.y + y
        return self.pos.y
        
# Square shaped piece.
class SquarePiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(3, -1)
        self.grid = [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]

# Long shaped piece.
class IPiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(3, -2)
        self.grid = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        
# J shaped piece.
class JPiece(Piece):
    
    # Initialize.
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(3, -1)
        self.grid = [[0, 0, 0, 0],
                     [2, 2, 2, 0],
                     [0, 0, 2, 0],
                     [0, 0, 0, 0]]
        
# L shaped piece
class LPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(2, -1)
        self.grid = [[0, 0, 0, 0],
                     [0, 2, 2, 2],
                     [0, 2, 0, 0],
                     [0 ,0, 0, 0]]
        
# T shaped piece.
class TPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(2, -2)
        self.grid = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]]
        
# S shaped piece.
class SPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(2, -1)
        self.grid = [[0, 0, 0, 0, 0],
                     [0, 0, 3, 3, 0],
                     [0, 3, 3, 0, 0],
                     [0, 0, 0, 0, 0]]
                
# Z shaped piece.
class ZPiece(Piece):
    
    # Initialize
    def __init__(self):
        Piece.__init__(self)
        self.pos.set(2, -1)
        self.grid = [[0, 0, 0, 0, 0],
                     [0, 3, 3, 0, 0],
                     [0, 0, 3, 3, 0],
                     [0, 0, 0, 0, 0]]
        
        