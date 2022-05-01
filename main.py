from pygame.locals import QUIT
import pygame


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)


main_screen = pygame.display.set_mode((600, 600))
main_screen.fill(BLACK)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        pygame.display.flip()            


main()