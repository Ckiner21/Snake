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
        self.direction = (0,0)  # (delta_y, delta_x) with 0,0 with -y being up
    
    def add_node(self):
        # We copy the list because otherwise tail_pos will change with tail as 
        # it is updated due to python being pass by reference
        tail_pos = self.tail.pos.copy()
        self.update_pos()
        new_node = Node(tail_pos)
        self.tail.next = new_node
        old_tail = self.tail
        self.tail = new_node
        self.tail.prev = old_tail

    def update_pos(self):
        # We copy the list for the same reason as in add_node
        last_pos = self.head.pos.copy()
        self.head.pos[0] += self.direction[0]
        self.head.pos[1] += self.direction[1]
        curr = self.head.next
        while curr is not None:
            tmp = curr.pos.copy()
            curr.pos = last_pos
            last_pos = tmp
            curr = curr.next
            

class Game:
    def __init__(self, screen, board_size=20):
        self.BLACK = pygame.Color(0, 0, 0)
        self.RED = pygame.Color(255, 0 , 0)
        self.GREEN = pygame.Color(0, 255, 0)

        self.SCREEN_SIZE = screen.get_height()
        self.CELL_SIZE = self.SCREEN_SIZE//board_size
        self.board_size = board_size
        CENTER = board_size//2

        self.snake = Snake([CENTER, CENTER])
        self.score = 1

        apple_x = randint(1,board_size-2)  # Account for walls, pixels start counting at zero
        apple_y = randint(1,board_size-2)
        self.apple = (apple_y, apple_x)

        self.main_screen = screen
        self.game_surface = self.init_board(self.main_screen)
    
    def init_board(self, screen):
        surface = pygame.Surface(screen.get_size())
        surface.fill(self.BLACK)

        border0 = pygame.Rect(0, 0, self.SCREEN_SIZE, self.CELL_SIZE)
        pygame.draw.rect(surface, self.RED, border0)
        border1 = pygame.Rect(0, 0, self.CELL_SIZE, self.SCREEN_SIZE)
        pygame.draw.rect(surface, self.RED, border1)
        border2 = pygame.Rect(self.SCREEN_SIZE-self.CELL_SIZE, 0, self.CELL_SIZE, self.SCREEN_SIZE)
        pygame.draw.rect(surface, self.RED, border2)
        border3 = pygame.Rect(0, self.SCREEN_SIZE-self.CELL_SIZE, self.SCREEN_SIZE, self.CELL_SIZE)
        pygame.draw.rect(surface, self.RED, border3)
        
        self.draw_cell(self.apple, self.RED, surf=surface)
        self.draw_cell(self.snake.head.pos, self.GREEN, surf=surface)
        return surface

    def update(self):
        new_head =[self.snake.head.pos[0] + self.snake.direction[0],
                   self.snake.head.pos[1] + self.snake.direction[1]]
        for i in new_head:  # Check if snake head would be in wall
            if i == 0 or i == self.board_size - 1:
                return -1
        curr = self.snake.head.next
        while curr is not None:  # Make sure the snake is not colliding with itself
            if new_head == curr.pos:
                return -1
            curr = curr.next

        if new_head == list(self.apple):  # The add node function updates the pos, so no need
            self.snake.add_node()
            self.score += 1
            colliding = True
            while colliding: # Make sure the apple is not colliding with the snake
                apple_x = randint(1,self.board_size-2)
                apple_y = randint(1,self.board_size-2)
                apple = (apple_y, apple_x)
                colliding = False
                while curr is not None:  
                    if apple == curr.pos:
                        colliding = True
                        break
                    curr = curr.next

            self.apple = apple
            self.draw_cell(self.apple, self.RED)
        else:  # Draw a black rectangle over the previous tail pos, update snake pos
            last_tail_pos = self.snake.tail.pos
            self.draw_cell(last_tail_pos, self.BLACK)
            self.snake.update_pos()
        
        self.draw_cell(self.snake.head.pos, self.GREEN)
        self.main_screen.blit(self.game_surface, (0,0))
        return None

    def convert(self, cell) -> tuple[int]:
        """The game is split into 'cells', so this converts 
           the cell into actual pixel coordinates"""
        coords = ()
        for i in cell:
            coords += (i*self.CELL_SIZE,)
        return coords

    def draw_cell(self, cell, color, surf=None):
        # We do this here as opposed to in the define statement because this
        # function is called when self.game_surf is being created
        if surf is None:
            surf = self.game_surface
        left, top = self.convert(cell)
        cell_rect = pygame.Rect(left, top, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(surf, color, cell_rect)
    