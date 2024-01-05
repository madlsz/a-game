import pygame
import random

pygame.init()

GAME_WIDTH = 500*0.8
GAME_HEIGHT = 1000*0.8
TILE_HEIGHT = GAME_HEIGHT/20
TILE_WIDTH = GAME_WIDTH/10

FPS = 30

class Tile():
    def __init__(self, screen, x, y, width, height, color = None):
        self.screen = screen
        self.rect = pygame.Rect(x,y,width,height)
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

moving_tiles = [Tile(screen,0,0,TILE_WIDTH,TILE_HEIGHT)]
static_tiles = []

# Run until the user asks to quit
running = True
while running:
    clock.tick(FPS)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keys = pygame.key.get_pressed()
    elapsed_time = pygame.time.get_ticks() - start_time_gravity
    if elapsed_time >= 650:
        start_time_gravity = pygame.time.get_ticks()
        # update_gravity()
        # doesnt work for now, it has to be done by editing the elapsed time value and not by speed
        # if keys[pygame.K_DOWN]:
        #     test_tile.move_y(test_tile.height*2)
        # else:
        for tile in moving_tiles:
            tile.move_y(tile.height)

    elapsed_time = pygame.time.get_ticks() - start_time_movement
    if elapsed_time >= 30:
        keys = pygame.key.get_pressed()
        start_time_movement = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            for tile in moving_tiles:
                tile.move_x(tile.width)
        if keys[pygame.K_LEFT]:
            for tile in moving_tiles:
                tile.move_x(-tile.width)

    # Fill the background with white
    screen.fill((50, 50, 50))
    
    at_bottom = False
    for tile in moving_tiles:
        if tile.y + tile.height >= screen.get_height():
            at_bottom = True
            break
        else:
            for static_tile in static_tiles:
                if tile.y + tile.height >= static_tile.y and tile.x >= static_tile.x and tile.x + tile.width <= static_tile.x+static_tile.width:
                    at_bottom = True
                    break
            if at_bottom:
                break
    if at_bottom:
        for tile in moving_tiles:
            static_tiles.append(tile)
        moving_tiles = [Tile(screen, 0,0,TILE_WIDTH,TILE_HEIGHT)]

    for tile in moving_tiles:
        tile.draw()
    for tile in static_tiles:
        tile.draw()
            
    # Flip the display
    # pygame.display.flip()
    pygame.display.update()

# Done! Time to quit.
pygame.quit()