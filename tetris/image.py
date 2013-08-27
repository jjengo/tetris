# Author: Jonathan Jengo

import os
import pygame
from .util import Point, Dimension

# Image dimensions
BlockSize = Dimension(20, 20)
BackgroundSize = Dimension(480, 450)
    
# Load an image from the file system
def load(filename):
    return pygame.image.load(os.path.join("images", filename)).convert()

# Image gallery
class Gallery:
    
    # Initialize
    def __init__(self):
        self.background = load("blue-background.png")
        self.blocks = {}
        
        blocksheet = SpriteSheet("blocks.png")
        for level in range(11):
            blockset = []
            for index in range(3):
                sub = blocksheet.subimage(level * BlockSize.width, index * BlockSize.height, BlockSize.width, BlockSize.height)
                blockset.append(Block(sub))
            self.blocks[level] = blockset
        
    # Render the background.
    def renderBackground(self, gfx):
        gfx.blit(self.background, (0, 0))

    # Render a block with level & index at specified grid point.
    def renderBlock(self, gfx, level, index, pt):
        if level in self.blocks and index >= 0 and index < 3:
            self.blocks[level][index].render(gfx, pt)

# A block image
class Block:
    
    # Initialize
    def __init__(self, image):
        self.image = image
        
    # Render the block at specified grid [x,y] indices
    def render(self, gfx, pt):
        pos = self.gridToPos(pt)
        gfx.blit(self.image, pos.tuple())
        
    # Convert grid point to its [x,y] position coordinates
    def gridToPos(self, pt):
        x = pt.x * BlockSize.width + 140
        y = pt.y * BlockSize.height + 40
        return Point(x, y)
    
# Container for a sprite sheet image
class SpriteSheet:
    
    # Initialize
    def __init__(self, filename):
        self.sheet = load(filename)
        
    # Get a subimage from the sheet.
    def subimage(self, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image