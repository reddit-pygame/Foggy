import os
import pygame as pg
import tools


SCREEN_SIZE = (1280, 720)
ORIGINAL_CAPTION = "Pygame Challenge"

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))

for num in range(1, 5):
    img = GFX["tree{}".format(num)]
    curvy = pg.Rect(0, 0, 128, 128)
    straight = pg.Rect(128, 0, 96, 128)
    GFX["curvy-tree{}".format(num)] = img.subsurface(curvy)
    GFX["straight-tree{}".format(num)] = img.subsurface(straight)