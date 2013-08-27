# Author: Jonathan Jengo

import os
import pygame

# Load a sound from the file system
def load(filename):
    return pygame.mixer.Sound(os.path.join("sounds", filename))

# Various sounds
class Sound:
    Clear, Drop, GameOver, Lateral, LevelUp, Rotate, Select, Start, Tetris, Music = range(10)

# Sound mixer
class Mixer:
    
    # Initialize
    def __init__(self):
        self.sounds = {}
        self.sounds[Sound.Clear] = load("clear.wav")
        self.sounds[Sound.Drop] = load("drop.wav")
        self.sounds[Sound.GameOver] = load("gameover.wav")
        self.sounds[Sound.Lateral] = load("lateralmove.wav")
        self.sounds[Sound.LevelUp] = load("levelup.wav")
        self.sounds[Sound.Rotate] = load("rotate.wav")
        self.sounds[Sound.Select] = load("select.wav")
        self.sounds[Sound.Start] = load("start.wav")
        self.sounds[Sound.Tetris] = load("tetris.wav")
        self.sounds[Sound.Music] = load("tetrismidi1.mid")
        self.looping = {}
        
    # Play a sound
    def play(self, key, loops = 0):
        self.sounds[key].stop()
        if loops == -1:
            self.loop(key)
        else:
            self.sounds[key].play(loops)
            
    # Play a looping sound
    def loop(self, key):
        if not key in self.looping or not self.looping[key]:
            self.sounds[key].play(-1)
            self.looping[key] = True

    # Stop playing a sound
    def stop(self, key):
        self.sounds[key].stop()
        if key in self.looping:
            self.looping[key] = False
                        
    # Pause all playback of sounds
    def pause(self):
        pygame.mixer.pause()
        
    # Resume all playback of sounds
    def unpause(self):
        pygame.mixer.unpause()
            
    # Stop playback of all sounds
    def stopall(self):
        for key in self.looping:
            self.sounds[key].stop()
            self.looping[key] = False
            
    # Play correct sound for placed piece.
    def playDropped(self, cleared):
        if cleared == 4:
            self.play(Sound.Tetris)
        elif cleared > 0:
            self.play(Sound.Clear)
        else:
            self.play(Sound.Drop)
            