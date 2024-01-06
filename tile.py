import pygame
import random

class Tile():
    pk = 0
    def __init__(self, screen, x, y, color = None):
        self.pk = Tile.pk
        Tile.pk += 1
        self.screen = screen
        self.rect = pygame.Rect(x,y,screen.get_width()/10,screen.get_height()/20)
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def move_x(self, x):
        if self.rect.x + self.rect.width + x <= self.screen.get_width() and self.rect.x + x >= 0:
            self.rect.x += x

    def move_y(self, y):
        if self.rect.y + self.rect.height + y <= self.screen.get_height() and self.rect.y + y >= 0:
            self.rect.y += y

    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    # @y.setter
    # def y(self, new_y):
    #     self.rect.y = new_y
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height
    
    # def at_bottom(self):
    #     return False