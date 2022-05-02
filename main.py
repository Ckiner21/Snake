from sys import exit
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN
import pygame
from game_objs import Game
import buttons


def center(surf_to_draw: pygame.Surface, surf: pygame.Surface) -> int:
    """Returns an integer representing an x coordinate that will place 
       surf_to_draw in the center of surf if the left side of surf_to_draw is 
       placed at x"""
    w1 = surf.get_width()
    w2 = surf_to_draw.get_width()
    return (w1//2) - (w2//2)


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)


main_surface = pygame.display.set_mode((600, 600))
main_surface.fill(BLACK)
icon = pygame.image.load("Sprites/Icon.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake in Pygame")


clock = pygame.time.Clock()


def menu():
    start_screen = pygame.Surface((600, 600))
    start_screen.fill(BLACK)
    title = pygame.image.load("Sprites/Title.png")
    title_x = center(title, main_surface)
    start_screen.blit(title, (title_x, 60))
    start_button = buttons.Button(sprite="Sprites/Play_Button.png")
    start_x = center(start_button.sprite, main_surface)
    start_button.draw(start_screen, (start_x, 300))
    main_surface.blit(start_screen, (0, 0))

    game_started = False
    while game_started == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if buttons.clicked(start_button, event.pos) is not None:
                    game_started = True
        pygame.display.flip()  

    return


def game_loop():
    game = Game(main_surface)
    game.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                key_direction = {1073741906: (0, -1), 1073741903: (1, 0),
                                 1073741905: (0, 1), 1073741904: (-1, 0)}
                new_direction = key_direction.get(event.key)
                negative = lambda x: -x
                if new_direction is not None:
                    if game.snake.direction != tuple(map(negative, new_direction)):  # Check that player is not trying to do 180 turn
                        game.snake.direction = new_direction

        game_state = game.update()
        if game_state is not None:  # We do this here instead of in the while logic to stop the game from rendering the snake in a wall
            break
        
        clock.tick(6.5)
        pygame.display.flip()
    
    del game


def end():
    end_screen = pygame.Surface((600, 600))
    end_screen.fill(BLACK)
    end_banner = pygame.image.load("Sprites/Game_over.png")
    banner_x = center(end_banner, main_surface)
    end_screen.blit(end_banner, (banner_x, 60))
    replay = buttons.Button(sprite="Sprites/Replay_Button.png")
    replay_x = center(replay.sprite, main_surface)
    replay.draw(end_screen, (replay_x, 300))
    main_surface.blit(end_screen, (0, 0))

    game_started = False
    while game_started == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if buttons.clicked(replay, event.pos) is not None:
                    game_started = True
        pygame.display.flip()  

    return


def main():
    menu()
    while True:
        game_loop()
        end()
main()