import pygame
import random
import tetrominos

pygame.init()

GAME_WIDTH = 500*0.8
GAME_HEIGHT = 1000*0.8

FPS = 30

class Entity():
    def __init__(self,screen, tetromino):
        self.screen = screen
        self.tiles = [Tile(screen, 0,0,tetromino.color), Tile(screen, screen.get_width()/10,0,tetromino.color)]
        self.tetromino = tetromino

    def move_x(self, x):
        for tile in self.tiles:
            if not (tile.x + tile.width + x <= self.screen.get_width() and tile.x + x >= 0):
                return
        for tile in self.tiles:
            tile.move_x(x)



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


# Set up the drawing window
screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
clock = pygame.time.Clock()
start_time_movement = pygame.time.get_ticks()
start_time_gravity = pygame.time.get_ticks()

moving_tiles = [Entity(screen, tetrominos.create_instance("O"))]
static_tiles = []
elapsed_time_timeout = 600
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    elapsed_time = pygame.time.get_ticks() - start_time_gravity
    if elapsed_time >= elapsed_time_timeout:
        start_time_gravity = pygame.time.get_ticks()
        if keys[pygame.K_DOWN]:
            elapsed_time_timeout = 100
        else:
            elapsed_time_timeout = 600
        for entity in moving_tiles:
            for tile in entity.tiles:
                tile.move_y(tile.height)

    elapsed_time = pygame.time.get_ticks() - start_time_movement
    if elapsed_time >= 30:
        start_time_movement = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            for entity in moving_tiles:
                entity.move_x(entity.tiles[0].width)
        if keys[pygame.K_LEFT]:
            for entity in moving_tiles:
                entity.move_x(-entity.tiles[0].width)

        at_bottom = False
        for entity in moving_tiles:
            for tile in entity.tiles:
                if tile.y + tile.height >= screen.get_height():
                    at_bottom = True
                    break
                else:
                    for static_entity in static_tiles:
                        for static_tile in static_entity.tiles:
                            if tile.y + tile.height >= static_tile.y and tile.x >= static_tile.x and tile.x + tile.width <= static_tile.x+static_tile.width:
                                at_bottom = True
                                break
                    if at_bottom:
                        break
            if at_bottom:
                break
        if at_bottom:
            for entity in moving_tiles:
                static_tiles.append(entity)
            moving_tiles = [Entity(screen, tetrominos.create_instance("O"))]

    # drawing section
            
    # Fill the background with white
    screen.fill((50, 50, 50))
    
    for entity in moving_tiles:
        for tile in entity.tiles:
            tile.draw()
    for entity in static_tiles:
        for tile in entity.tiles:
            tile.draw()
            
    pygame.display.update()

pygame.quit()