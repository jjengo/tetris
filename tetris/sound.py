import os
import pygame

def load(filename):
    return pygame.mixer.Sound(os.path.join("sounds", filename))

def load_music(filename):
    return pygame.mixer.music.load(os.path.join("sounds", filename))

# Various sounds
class Sound(object):
    Clear, Drop, GameOver, Lateral, LevelUp, Rotate, Select, Start, Tetris = range(9)

# Sound mixer
class Mixer(object):
    
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
        #self.music = loadMusic("tetrismusic.mp3")
        self.looping = {}
        
    # Play a sound
    def play(self, key, loops = 0):
        self.sounds[key].stop()
        if loops == -1:
            self.loop(key)
        else:
            self.sounds[key].play(loops)
            
    # Play music
    def loop_music(self):
        pass
        #pygame.mixer.music.play(-1, 0.0)
            
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
            
    # Stop music
    def stop_music(self):
        pass
        #pygame.mixer.music.stop()
                        
    # Pause all playback of sounds
    def pause(self):
        pygame.mixer.pause()
        
    # Resume all playback of sounds
    def unpause(self):
        pygame.mixer.unpause()
            
    # Stop playback of all sounds
    def stop_all(self):
        self.stop_music()
        for key in self.looping:
            self.sounds[key].stop()
            self.looping[key] = False
            
    # Play correct sound for placed piece.
    def play_dropped(self, cleared):
        if cleared == 4:
            self.play(Sound.Tetris)
        elif cleared > 0:
            self.play(Sound.Clear)
        else:
            self.play(Sound.Drop)
            