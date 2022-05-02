from pygame.locals import QUIT, MOUSEBUTTONDOWN
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


main_screen = pygame.display.set_mode((600, 600))
main_screen.fill(BLACK)
icon = pygame.image.load("Sprites/Icon.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake Game")


start_screen = pygame.Surface((600, 600))
start_screen.fill(BLACK)
title = pygame.image.load("Sprites/Title.png")
title_x = center(title, main_screen)
start_screen.blit(title, (title_x, 60))
start_button = buttons.Button(sprite="Sprites/Play_Button.png", func=print)
start_x = center(start_button.sprite, main_screen)
start_button.draw(start_screen, (start_x, 300))
main_screen.blit(start_screen, (0, 0))


game = Game(main_screen)


def main():
    game_started = False
    while game_started == False:  # This is the loop for the start screen
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if buttons.clicked(start_button, event.pos) is not None:
                    start_button.click("done")
                    game_started = True
        pygame.display.flip()   

    game.update()
    while True:   # Main loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        pygame.display.flip()
        
main()