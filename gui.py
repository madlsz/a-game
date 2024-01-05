import pygame
pygame.init()

GAME_WIDTH = 500*0.8
GAME_HEIGHT = 1000*0.8
TILE_HEIGHT = GAME_HEIGHT/20
TILE_WIDTH = GAME_WIDTH/10

FPS = 30

class Tile():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = (200,88,50)
        self.y_speed = 2
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def move_x(self, x):
        if self.rect.x + self.rect.width + x <= GAME_WIDTH and self.rect.x + x >= 0:
            self.rect.x += x

    def move_y(self, y):
        if self.rect.y + self.rect.height + y <= GAME_HEIGHT and self.rect.y + y >= 0:
            self.rect.y += y

    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, new_y):
        self.rect.y = new_y
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height
    
    def at_bottom(self):
        return False

test_tile = Tile(0,0,TILE_WIDTH,TILE_HEIGHT)

moving_tiles = []
static_tiles = []


# Set up the drawing window
screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
clock = pygame.time.Clock()
start_time_horizontal = pygame.time.get_ticks()
start_time_vertical = pygame.time.get_ticks()

# Run until the user asks to quit
running = True
while running:
    clock.tick(FPS)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    elapsed_time = pygame.time.get_ticks() - start_time_vertical
    if elapsed_time >= 800:
        start_time_vertical = pygame.time.get_ticks()
        # doesnt work for now, it has to be done by editing the elapsed time value and not by speed
        # if keys[pygame.K_DOWN]:
        #     test_tile.move_y(test_tile.height*2)
        # else:
        test_tile.move_y(test_tile.height)

    keys = pygame.key.get_pressed()
    elapsed_time = pygame.time.get_ticks() - start_time_horizontal
    if elapsed_time >= 30:
        start_time_horizontal = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            test_tile.move_x(test_tile.width)
        if keys[pygame.K_LEFT]:
            test_tile.move_x(-test_tile.width)

    # Fill the background with white
    screen.fill((50, 50, 50))

    test_tile.draw()
    # test_tile.move_y(test_tile.y_speed)
    if test_tile.y + test_tile.width >= GAME_HEIGHT:
        test_tile.y = 0
    # Flip the display
    # pygame.display.flip()
    pygame.display.update()

# Done! Time to quit.
pygame.quit()