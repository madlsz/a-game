import pygame
import copy

import tetrominos
import tile

pygame.init()

GAME_WIDTH = 500*0.8
GAME_HEIGHT = 1000*0.8

FPS = 30

# Set up the drawing window
screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
clock = pygame.time.Clock()
start_time_movement = pygame.time.get_ticks()
start_time_gravity = pygame.time.get_ticks()

# entity = tetrominos.create_instance("O", screen)
# static_entities = []
entities = []
entities.append(tetrominos.create_instance("O", screen))
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
        for tile in entity.tiles:
            tile.move_y(tile.height)

    elapsed_time = pygame.time.get_ticks() - start_time_movement
    if elapsed_time >= 30:
        start_time_movement = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            for entity in [e for e in entities if not e.static]:
                entity.move_x(entity.tiles[0].width)
        if keys[pygame.K_LEFT]:
            for entity in [e for e in entities if not e.static]:
                entity.move_x(-entity.tiles[0].width)

        at_bottom = False
        for entity in [e for e in entities if not e.static]:
            for tile in entity.tiles:
                if tile.y + tile.height >= screen.get_height():
                    at_bottom = True
                    break
                else:
                    for static_entity in [e for e in entities if e.static]:
                        for static_tile in static_entity.tiles:
                            if tile.y + tile.height >= static_tile.y and tile.x >= static_tile.x and tile.x + tile.width <= static_tile.x+static_tile.width:
                                at_bottom = True
                                break
                    if at_bottom:
                        break
        if at_bottom:
            [entity for entity in entities if not entity.static][0].static = True
            entities.append(tetrominos.create_instance("O", screen))

    # drawing section
            
    # Fill the background with white
    screen.fill((50, 50, 50))
    
    for entity in entities:
        for tile in entity.tiles:
            tile.draw()
            
    pygame.display.update()

pygame.quit()