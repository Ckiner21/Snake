from random import randint
import pygame


class Node:
    def __init__(self, pos=None, next=None, prev=None):
        self.pos = pos
        self.next = next
        self.prev = prev


class Snake:
    def __init__(self, start_pos=None):
        self.head = Node(pos=start_pos)
        self.tail = self.head
        self.direction = (-1,0)  # (delta_y, delta_x) with 0,0 with -y being up
        self.score = 1
    
    def add_node(self):
        new_node = Node()
        self.tail.next = new_node
        self.tail = new_node
        self.score += 1


class Game:
    def __init__(self, screen, board_size=20):
        self.BLACK = pygame.Color(0, 0, 0)
        self.RED = pygame.Color(255, 0 , 0)
        self.GREEN = pygame.Color(0, 255, 0)
        self.SCRHEIGHT = screen.get_height()
        self.MARGIN = self.SCRHEIGHT//board_size

        CENTER = board_size//2
        self.snake = Snake((CENTER, CENTER))

        apple_x = randint(1,board_size-2)  # Account for walls, pixels start counting at zero
        apple_y = randint(1,board_size-2)
        self.apple = (apple_y, apple_x)

        self.main_screen = screen
        self.game_surface = self.init_board(self.main_screen)
    
    def init_board(self, screen):
        surface = pygame.Surface(screen.get_size())
        surface.fill(self.BLACK)

        border0 = pygame.Rect(0, 0, self.SCRHEIGHT, self.MARGIN)
        pygame.draw.rect(surface, self.RED, border0)
        border1 = pygame.Rect(0, 0, self.MARGIN, self.SCRHEIGHT)
        pygame.draw.rect(surface, self.RED, border1)
        border2 = pygame.Rect(self.SCRHEIGHT-self.MARGIN, 0, self.MARGIN, self.SCRHEIGHT)
        pygame.draw.rect(surface, self.RED, border2)
        border3 = pygame.Rect(0, self.SCRHEIGHT-self.MARGIN, self.SCRHEIGHT, self.MARGIN)
        pygame.draw.rect(surface, self.RED, border3)
        
        return surface

    def update(self):
        #update head pos
        #check if head is in margin, hitting snake, or hitting apple
        #if in margin or hitting snake, end game
        #if hitting apple, score += 1, append new node,
        self.main_screen.blit(self.game_surface, (0,0))

    def convert(self, cell) -> tuple[int]:
        coords = ()
        for i in cell:
            coords += (i*self.margin,)
        return coords

    