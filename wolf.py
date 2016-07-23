from random import choice, randint
from itertools import cycle

import pygame as pg

from prepare import GFX, SCREEN_RECT
from tools import strip_from_sheet as strip


class Wolf(pg.sprite.Sprite):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    footprint_info = ((6, 24, 46, 8), (13, 24, 46, 8), (5, 11, 23, 8), (5, 46, 23, 8))
    footprints = {d: i for d, i in zip(directions, footprint_info)}
    
    def __init__(self, pos, *groups):
        super(Wolf, self).__init__(*groups)
        self.pos = pos
        self.image_dict = {
                (-1, 0): cycle(strip(GFX["wolfleft"], (0, 0), (64, 32), 5)),
                (1, 0): cycle(strip(GFX["wolfright"], (0, 0), (64, 32), 5)), 
                (0, 1): cycle(strip(GFX["wolfdown"], (0, 0), (32, 64), 4)),
                (0, -1): cycle(strip(GFX["wolfup"], (0, 0), (32, 64), 4))}
        self.direction = choice(self.directions)
        self.images = self.image_dict[self.direction]
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 3
        self.move_time = randint(500, 2000)
        self.frame_time = 60
        self.frame_timer = 0
        
    def set_footprint(self):
        x, y, w, h = self.footprints[self.direction]
        self.footprint = pg.Rect(self.rect.x + x, self.rect.y + y, w, h)
        
    def collide(self, other):     
        rect = other.footprint
        offsets = {
                (-1, 0): (rect.right - self.footprint.left, 0),
                (1, 0): (rect.left - self.footprint.right, 0),
                (0, -1): (0, rect.bottom - self.footprint.top),
                (0, 1): (0, rect.top - self.footprint.bottom)}
        self.rect.move_ip(offsets[self.direction])
        self.pos = self.rect.center
        self.set_footprint()
        self.redirect()
        
    def redirect(self):
        self.direction = choice(self.directions)
        self.move_time = randint(500, 2000)
        self.images = self.image_dict[self.direction]
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=self.pos)
        self.set_footprint()
        
    def update(self, dt):
        self.move_time -= dt
        if self.move_time <= 0:
            self.redirect()
        self.frame_timer += dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images)            
        vx, vy = self.direction
        self.pos = self.pos[0] + vx, self.pos[1] + vy
        self.rect.center = self.pos
        r = self.rect.clamp(SCREEN_RECT)
        if r != self.rect:
            self.rect = r
            self.pos = self.rect.center
        self.set_footprint()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)