import moderngl
import pygame
from typing import Optional, Any
from json import load, dump
from os.path import isfile

pygame.init()


class Config:
    # constants
    rSCREEN_WIDTH = pygame.display.Info().current_w if pygame.display.Info().current_w else 1920
    rSCREEN_HEIGHT = pygame.display.Info().current_h if pygame.display.Info().current_h else 1080
    # SCREEN_WIDTH = pygame.display.Info().current_w if pygame.display.Info().current_w else 1920
    # SCREEN_HEIGHT = pygame.display.Info().current_h if pygame.display.Info().current_h else 1080
    CAMERA_SPEED = 500
    SQUARE_SIZE = 50
    PARTICLE_SPEED = 10

    # colors
    #
    # each color theme requires a hallway color, a background color, and at least one square color
    # optionally, the color theme provides an hp_bar_border color (default 10, 9, 8),
    # an hp_bar_background color (default 34, 51, 59), and a list
    # of hp_bar_fill colors (default (156, 198, 155), (189, 228, 168), (215, 242, 186))
    #
    color_themes = {
        "dark_modern": {
            "hallway": pygame.Color(40, 44, 52),
            "background": pygame.Color(24, 26, 30),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },

        "dark": {
            "hallway": pygame.Color(214, 209, 205),
            "background": pygame.Color(60, 63, 65),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        # credits to TheCodingCrafter for these themes
        "light": {
            "hallway": pygame.Color(60, 63, 65),
            "background": pygame.Color(214, 209, 205),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "rainbow": {
            "hallway": pygame.Color((214, 209, 205)),
            "background": pygame.Color((60, 63, 65)),
            "square": [
                pygame.Color(0, 0, 0)
            ]
        },
        "autumn": {
            "hallway": pygame.Color((252, 191, 73)),
            "background": pygame.Color((247, 127, 0)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "winter": {
            "hallway": pygame.Color((202, 240, 255)),
            "background": pygame.Color((0, 180, 216)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "spring": {
            "hallway": pygame.Color((158, 240, 26)),
            "background": pygame.Color((112, 224, 0)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "magenta": {
            "hallway": pygame.Color((239, 118, 116)),
            "background": pygame.Color((218, 52, 77)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "monochromatic": {
            "hallway": pygame.Color((255, 255, 255)),
            "background": pygame.Color((0, 0, 0)),
            "square": [
                pygame.Color(80, 80, 80),
                pygame.Color(150, 150, 150),
                pygame.Color(100, 100, 100),
                pygame.Color(200, 200, 200)
            ]
        },
        "green-screen-hallway": {
            "hallway": pygame.Color(0, 255, 0),
            "background": pygame.Color(60, 63, 65),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "green-screen-background": {
            "hallway": pygame.Color(60, 63, 65),
            "background": pygame.Color(0, 255, 0),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        }
    }

    # intended configurable settings
    # SCREEN_WIDTH = pygame.display.Info().current_w if pygame.display.Info().current_w else 1920
    # SCREEN_HEIGHT = pygame.display.Info().current_h if pygame.display.Info().current_h else 1080
    SCREEN_WIDTH = 1080  # Custom width
    SCREEN_HEIGHT = 1920  # Custom height
    theme: Optional[str] = "dark_modern"
    seed: Optional[int] = None
    camera_mode: Optional[int] = 2
    start_playing_delay = 3000
    max_notes: Optional[int] = 1200
    bounce_min_spacing: Optional[float] = 30
    square_speed: Optional[int] = 700
    volume: Optional[int] = 80
    music_offset: Optional[int] = 0
    direction_change_chance: Optional[int] = 30
    hp_drain_rate = 10
    theatre_mode = True
    particle_trail = True
    shader_file_name = "none.glsl"
    do_color_bounce_pegs = True
    do_particles_on_bounce = True
    do_color_peg_effects = True

    # settings that are not configurable (yet)
    backtrack_chance: Optional[float] = 0.02
    backtrack_amount: Optional[int] = 40
    rainbow_speed: Optional[int] = 30
    square_swipe_anim_speed: Optional[int] = 4
    particle_amount = 10
    language = "english"

    # other random stuff
    current_song = None
    ctx: moderngl.Context = None
    glsl_program: moderngl.Program = None
    render_object: moderngl.VertexArray = None
    screen: pygame.Surface = None
    dt = 0.01

    # ascii shader
    ascii_tex: moderngl.Texture = None

    # keys to save and load
    save_attrs = ["theme", "seed", "camera_mode", "start_playing_delay", "max_notes", "bounce_min_spacing",
                  "square_speed", "volume", "music_offset", "direction_change_chance", "hp_drain_rate", "theatre_mode",
                  "particle_trail", "shader_file_name", "do_color_bounce_pegs", "do_particles_on_bounce", "language",
                  "SCREEN_WIDTH", "SCREEN_HEIGHT", "rainbow_glow", "rainbow_glow_speed", 
                  "trail_particle_size_min", "trail_particle_size_max", "trail_color", 
                  "rainbow_trail", "rainbow_trail_speed", "do_color_peg_effects"]

    # glow effect settings
    square_glow = True
    square_glow_duration = 0.8
    glow_intensity = 15  # 1-40
    square_min_glow = 7
    border_color = pygame.Color(255, 255, 255)
    glow_color = pygame.Color(255, 255, 255)  # Change this for different glow color
    rainbow_glow = True  # Set to True for rainbow glow, False for static color
    rainbow_glow_speed = 50  # Lower = slower rainbow cycle

    # particle and trail settings
    particle_amount = 10
    trail_particle_size_min = 10  # Minimum trail particle size
    trail_particle_size_max = 20  # Maximum trail particle size
    trail_color = pygame.Color(255, 255, 0)  # Changed to white (255, 255, 255)
    particle_trail = True  # Enable/disable trail
    rainbow_trail = True  # Set to True for rainbow trail, False for static color
    rainbow_trail_speed = 50  # Lower = slower rainbow cycle

    # Add at the top of Config class
    USE_FILE_CONFIG = True  # When True, ignores settings.json and uses values directly from this file

    # Particle effect settings
    bounce_particle_size_min = 5
    bounce_particle_size_max = 20
    ring_particle_count = 12      # Number of particles in the expanding ring
    burst_particle_count = 15     # Number of particles in the burst
    sparkle_particle_count = 10    # Number of white sparkle particles
    ring_particle_speed = 12      # Base speed for ring particles
    burst_particle_speed = 25     # Max speed for burst particles
    sparkle_particle_speed = 15  # Base speed for sparkle particles


def get_colors():
    return Config.color_themes.get(Config.theme, "dark_modern")


def save_to_file(dat: Optional[dict[str, Any]] = None):
    # Skip saving if using file config
    if Config.USE_FILE_CONFIG:
        return
        
    if dat is None:
        dat = {k: getattr(Config, k) for k in Config.save_attrs}
    
    # Convert Color objects to RGB tuples before saving
    for key, value in dat.items():
        if isinstance(value, pygame.Color):
            dat[key] = (value.r, value.g, value.b)  # Convert Color to RGB tuple
            
    with open("./assets/settings.json", "w") as f:
        dump(dat, f, indent=4)


def load_from_file():
    # Skip loading from settings.json if USE_FILE_CONFIG is True
    if Config.USE_FILE_CONFIG:
        print("Using config.py values (USE_FILE_CONFIG = True)")
        return
        
    try:
        if isfile("./assets/settings.json"):
            with open("./assets/settings.json", "r") as f:
                data = load(f)
                for setting in data:
                    # Convert RGB tuples back to Color objects
                    if setting in ['trail_color', 'glow_color', 'border_color']:
                        if isinstance(data[setting], (list, tuple)):
                            data[setting] = pygame.Color(*data[setting])
                    setattr(Config, setting, data[setting])
        else:
            with open("./assets/settings.json", "w") as f:
                f.write('{}')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "config":
    load_from_file()
