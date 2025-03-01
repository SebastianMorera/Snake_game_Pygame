import pygame
import random
from pygame import Vector2


class Fruit:
    def __init__(
        self, screen: pygame.display, cell_size: int, cell_number: int
    ) -> None:
        """
        Initializes the fruit.
        Sets up the fruit's position, graphics, and sound effects.
        :param screen: The game screen.
        :param cell_size: The size of each cell in the game grid.
        :param cell_number: The number of cells in the game grid.
        """
        self.screen = screen
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.apple = pygame.image.load("assets/Graphics/apple.png").convert_alpha()
        self.x = None
        self.y = None
        self.pos = None
        self.randomize()

    def draw_fruit(self) -> None:
        """
        Draws the fruit on the game screen.
        Updates the fruit's graphics and draws it at its current position.
        """
        fruit_rect = pygame.Rect(
            int(self.pos.x * self.cell_size),
            int(self.pos.y * self.cell_size),
            self.cell_size,
            self.cell_size,
        )
        self.screen.blit(self.apple, fruit_rect)

    def randomize(self) -> None:
        """
        Randomizes the fruit's position.
        Sets the fruit's position to a new random location on the game grid.
        """
        self.x = random.randint(0, self.cell_number - 1)
        self.y = random.randint(0, self.cell_number - 1)
        self.pos = Vector2(self.x, self.y)
