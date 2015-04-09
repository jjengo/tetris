import sys
import pygame
from pygame.locals import *
from tetris.game import Tetris
from tetris.image import Gallery
from tetris.util import ScreenSize

class Core(object):
    
    Menu, Running, Paused, GameOver = range(4)

    def __init__(self, gfx):
        self.gfx = gfx
        self.keys = {}
        self.menu = Menu()
        self.gallery = Gallery()
        self.game = Tetris()
        self.state = Core.Menu
        self.time_to_menu = 0

    def run(self):
        
        clock = pygame.time.Clock()
        
        while True:
            
            self.keys = {}
            for event in pygame.event.get():
                self.handle_event(event)
                
            self.gfx.fill((0, 0, 0))
            
            # Game State: Menu
            if self.state == Core.Menu:
                self.menu.render(self.gfx, self.gallery)
            
            # Game State: Running
            elif self.state == Core.Running:
                self.game.process_key_events(self.keys)
                self.game.update()
                self.game.render(self.gfx, self.gallery)
            
            # Game State: Paused
            elif self.state == Core.Paused:
                self.game.render(self.gfx, self.gallery)
            
            # Game State: Game Over
            elif self.state == Core.GameOver:
                self.game.render(self.gfx, self.gallery)
            
            self.process_key_events()
            self.update()
            self.render()
            
            pygame.display.update()
            clock.tick(30)
            
    # Handle caught pygame event
    def handle_event(self, event):

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
    def process_key_events(self):
        
        if K_RETURN in self.keys:
            if self.state == Core.Menu:
                self.state = Core.Running
                self.game.newGame()
        
        if K_p in self.keys:
            if self.state == Core.Running:
                self.state = Core.Paused
                self.game.mixer.stop_music()
            elif self.state == Core.Paused:
                self.state = Core.Running
                self.game.mixer.loop_music()
    
    # Update all values
    def update(self):
        
        if self.state == Core.Running:
            if self.game.game_over():
                self.game.mixer.stop_all()
                self.state = Core.GameOver
                self.time_to_menu = 200
        elif self.state == Core.GameOver:
            self.time_to_menu -= 1
            if not self.time_to_menu:
                self.state = Core.Menu
    
    # Render values.
    def render(self):
        
        if self.state == Core.Paused:
            font = pygame.font.SysFont("OCR A Extended", 18)
            label = font.render("PAUSED", 1, (255, 255, 255))
            self.gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_width() / 2), 180))

class Menu(object):
    
    def render(self, gfx, gallery):
        
        bg = (0, 69, 134)
        fg = (225, 225, 225)
        
        # Splash.
        gfx.fill(bg)
        gfx.blit(gallery.splash, (10, 10))
        pygame.draw.aaline(gfx, fg, (10, 10), (470, 10), 1)
        pygame.draw.aaline(gfx, fg, (470, 10), (470, 279), 1)
        pygame.draw.aaline(gfx, fg, (10, 279), (470, 279), 1)
        pygame.draw.aaline(gfx, fg, (10, 10), (10, 279), 1)
        
        # Labels.
        font = pygame.font.SysFont("OCR A Extended", 20)
        label = font.render("Play Game", 1, fg)
        gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_width() / 2), 300))
        font = pygame.font.SysFont("OCR A Extended", 12)
        label = font.render("Jonathan Jengo", 1, fg)
        gfx.blit(label, ((ScreenSize[0] / 2) - (label.get_width() / 2), 425))
