from itertools import cycle

import pygame as pg

from prepare import GFX, SCREEN_RECT
from tools import strip_from_sheet as strip


class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(*groups)
        self.pos = pos        
        self.move_keys = {
                pg.K_LEFT: "left",
                pg.K_RIGHT: "right",
                pg.K_DOWN: "down",
                pg.K_UP: "up"}
        self.direct_to_velocity = {
                "left": (-1, 0),
                "right": (1, 0),
                "down": (0, 1),
                "up": (0, -1)}
        self.direction_stack = []
        self.direction = "left"
        self.last_direction = self.direction
        img_size = (32, 36)
        self.image_dict = {
                "left": cycle(strip(GFX["ranger_f"], (0, 108), img_size, 3)), 
                "right": cycle(strip(GFX["ranger_f"], (0,36), img_size, 3)), 
                "down": cycle(strip(GFX["ranger_f"], (0, 72), img_size, 3)), 
                "up": cycle(strip(GFX["ranger_f"], (0, 0), img_size, 3))}
        self.images = self.image_dict[self.direction]
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=self.pos)
        self.frame_time = 60
        self.frame_timer = 0
        self.speed = .1
        self.footprint = pg.Rect(0, 0, 30, 6)
        self.footprint.midbottom = self.rect.midbottom
        
    def collide(self, other):     
        rect = other.footprint
        offsets = {
                "left": (rect.right - self.footprint.left, 0),
                "right": (rect.left - self.footprint.right, 0),
                "up": (0, rect.bottom - self.footprint.top),
                "down": (0, rect.top - self.footprint.bottom)}
        self.rect.move_ip(offsets[self.direction])
        self.pos = self.rect.center
        self.footprint.midbottom = self.rect.midbottom

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in self.move_keys:
                d = self.move_keys[event.key]
                if d in self.direction_stack:
                    self.direction_stack.remove(d)
                self.direction_stack.append(d)
                self.direction = d
        elif event.type == pg.KEYUP:
            if event.key in self.move_keys:
                d = self.move_keys[event.key]
                if d in self.direction_stack:
                    self.direction_stack.remove(d)
                if self.direction_stack:
                    self.direction = self.direction_stack[-1]

    def update(self, dt):
        if self.direction != self.last_direction:
            self.images = self.image_dict[self.direction]
        self.last_direction = self.direction
        dx, dy = 0, 0
        if self.direction_stack:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_time:
                self.frame_timer -= self.frame_time
                self.image = next(self.images)
            vx, vy = self.direct_to_velocity[self.direction]
            dx = vx * self.speed * dt
            dy = vy * self.speed * dt
        self.pos = self.pos[0] + dx, self.pos[1] + dy
        self.rect.center = self.pos        
        r = self.rect.clamp(SCREEN_RECT)
        if r != self.rect:
            self.rect = r
            self.pos = self.rect.center
        self.footprint.midbottom = self.rect.midbottom
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)    
