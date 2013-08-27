# Author: Jonathan Jengo

import sys
import pygame
from pygame.locals import *
from . import image as Image
from .game import Tetris
from .image import Gallery

# Core engine
class Core:
    
    # Various game states
    Menu, Running, Paused, GameOver = range(4)
    
    # Initialize
    def __init__(self, gfx):
        self.gfx = gfx
        self.keys = {}
        self.gallery = Gallery()
        self.game = Tetris()
        self.state = Core.Running
        
    # Run the core engine.
    def run(self):
        
        clock = pygame.time.Clock()
        
        while True:
            
            self.keys = {}
            for event in pygame.event.get():
                self.handleEvent(event)
                
            self.gfx.fill((0, 0, 0))
            
            # Game State: Menu
            if self.state == Core.Menu:
                pass
            
            # Game State: Running
            elif self.state == Core.Running:
                self.game.processKeyEvents(self.keys)
                self.game.update()
                self.game.render(self.gfx, self.gallery)
            
            # Game State: Paused
            elif self.state == Core.Paused:
                pass
            
            # Game State: Game Over
            elif self.state == Core.GameOver:
                pass
            
            self.processKeyEvents()
            self.update()
            self.render(self.gfx)
            
            pygame.display.update()
            clock.tick(30)
            
    # Handle caught pygame event
    def handleEvent(self, event):

        # Handle exit events.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Handle key events.
        elif event.type == KEYDOWN:
            self.keys[event.key] = True
        elif event.type == KEYUP:
            if event.key in self.keys:
                del self.keys[event.key]
            
    # Process all relevant key events
    def processKeyEvents(self):
        pass
    
    # Update all values
    def update(self):
        pass
    
    # Render values.
    def render(self, gfx):
        pass
