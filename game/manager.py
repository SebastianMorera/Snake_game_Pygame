import pygame
import sys
from pygame import Vector2
from game.snake import Snake
from game.fruit import Fruit

GREEN_COLOR = (175, 215, 70)


class Manager:
    def __init__(self) -> None:
        """
        Initializes the game manager.
        Sets up the game window, font, and sound effects. Creates instances of the snake and fruit.
        """
        self.fps = 60
        self.cell_size = 40
        self.cell_number = 20

        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cell_number * self.cell_size, self.cell_number * self.cell_size)
        )
        pygame.display.set_caption("Snake")
        self.gameOver_sound = pygame.mixer.Sound("assets/Sound/game_over.wav")
        self.game_font = pygame.font.SysFont("comicsans", 25)
        self.apple = pygame.image.load("assets/Graphics/apple.png").convert_alpha()
        self.clock = pygame.time.Clock()
        self.screenUpdate = pygame.USEREVENT
        pygame.time.set_timer(self.screenUpdate, 150)

        self.snake = Snake(screen=self.screen, cell_size=self.cell_size)
        self.fruit = Fruit(
            screen=self.screen, cell_size=self.cell_size, cell_number=self.cell_number
        )

    def update(self) -> None:
        """
        Updates the game state.
        Moves the snake, checks for collisions with the fruit and the game boundaries, and updates the score.
        """
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self) -> None:
        """
        Draws the game elements.
        Draws the grass, snake, fruit, and score on the game screen.
        """
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self) -> None:
        """
        Checks for collisions between the snake and the fruit.
        If the snake collides with the fruit, updates the fruit position and plays a sound effect.
        """
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self) -> None:
        """
        Checks if the game has failed.
        If the snake collides with the game boundaries or itself, plays a sound effect and resets the game.
        """
        if (
            not 0 <= self.snake.body[0].x < self.cell_number
            or not 0 <= self.snake.body[0].y < self.cell_number
        ):
            if len(self.snake.body) != 3:
                self.play_gameOver_sound()
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                if len(self.snake.body) != 3:
                    self.play_gameOver_sound()
                self.game_over()

    def game_over(self) -> None:
        """
        Resets the game state.
        Resets the snake position and direction.
        """
        self.snake.reset()

    def draw_grass(self) -> None:
        """
        Draws the grass on the game screen.
        Creates a checkered pattern using green rectangles.
        """
        grass_color = (167, 209, 61)

        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        )
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        )
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

    def draw_score(self) -> None:
        """
        Draws the score on the game screen.
        Displays the current score using a font.
        """
        score_text = str(len(self.snake.body) - 3)

        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(self.cell_size * self.cell_number - 60)
        score_y = int(self.cell_size * self.cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        apple_rect = self.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 8,
            apple_rect.height,
        )

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.apple, apple_rect)

    def play_gameOver_sound(self) -> None:
        """
        Plays the game over sound effect.
        """
        self.gameOver_sound.play()

    def run_game(self) -> None:
        """
        Runs the game loop.
        Handles user input, updates the game state, and draws the game elements.
        """
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.screenUpdate:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_UP:
                        if self.snake.direction.y != 1:
                            self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction.y != -1:
                            self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction.x != 1:
                            self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction.x != -1:
                            self.snake.direction = Vector2(1, 0)

            self.screen.fill(pygame.Color(GREEN_COLOR))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()
