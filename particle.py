import random
from utils import *
import pygame


class Particle:
    SPEED_VARIATION = 4
    AGE_RATE = 20
    SLOW_DOWN_RATE = 1.2

    def __init__(self, pos: list[float], delta: list[float], is_trail: bool = False):
        self.pos = pos.copy()
        self.creation_time = pygame.time.get_ticks()
        self.color = None  # Initialize color first
        self.alpha = None  # Initialize alpha for all particles
        
        if is_trail:
            self.size = random.randint(Config.trail_particle_size_min, Config.trail_particle_size_max)
            if Config.rainbow_trail:
                # Initialize with a color based on time
                rainbow_color = pygame.Color(0, 0, 0)
                hue = (self.creation_time / Config.rainbow_trail_speed) % 360
                rainbow_color.hsva = (hue, 100, 100, 100)
                self.color = rainbow_color
            else:
                self.color = Config.trail_color  # Use the configured trail color
        else:
            self.size = random.randint(7, 14)
            if isinstance(self.color, pygame.Color) and self.color == pygame.Color(75, 0, 130):
                self.color = pygame.Color(75, 0, 130)  # Indigo for hit particles
                self.alpha = 255  # Only set alpha for indigo particles
            else:
                self.color = get_colors()["hallway"]  # Default color for other particles
            
        self.delta = delta.copy()
        self.delta[0] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION)/8
        self.delta[1] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION)/8
        
    def age(self):
        self.size -= Particle.AGE_RATE*Config.dt
        self.x += self.delta[0] * Config.PARTICLE_SPEED
        self.y += self.delta[1] * Config.PARTICLE_SPEED
        self.delta[0] /= (Particle.SLOW_DOWN_RATE+FRAMERATE) * Config.dt
        self.delta[1] /= (Particle.SLOW_DOWN_RATE+FRAMERATE) * Config.dt
        
        # Only update rainbow color if rainbow trail is enabled
        if Config.rainbow_trail and hasattr(self, 'creation_time'):
            rainbow_color = pygame.Color(0, 0, 0)
            hue = ((pygame.time.get_ticks() + self.creation_time) / Config.rainbow_trail_speed) % 360
            rainbow_color.hsva = (hue, 100, 100, 100)
            self.color = rainbow_color
        elif hasattr(self, 'creation_time'):  # If it's a trail particle but not rainbow
            self.color = Config.trail_color  # Keep using the configured trail color
            
        # Fade out indigo particles
        if self.alpha is not None:
            self.alpha -= 600 * Config.dt
            if isinstance(self.color, pygame.Color):
                self.color.a = max(0, int(self.alpha))
            
        return self.size <= 0 or (self.alpha is not None and self.alpha <= 0)

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, val: float):
        self.pos[0] = val

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, val: float):
        self.pos[1] = val

    @property
    def rect(self):
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *(2*[self.size]))