
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetromino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]]  # O
]

# Generate all rotations for each shape
ROTATIONS = []
for shape in SHAPES:
    rotations = [shape]
    current_shape = shape
    for _ in range(3):
        current_shape = [list(row) for row in zip(*current_shape[::-1])]
        if current_shape not in rotations:
            rotations.append(current_shape)
    ROTATIONS.append(rotations)

COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 255, 0)   # Yellow
]

class Tetromino:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.rotations = ROTATIONS[shape_index]
        self.rotation = 0
        self.shape = self.rotations[self.rotation]
        self.color = COLORS[shape_index]

    def rotate(self, clockwise=True):
        if clockwise:
            self.rotation = (self.rotation + 1) % len(self.rotations)
        else:
            self.rotation = (self.rotation - 1 + len(self.rotations)) % len(self.rotations)
        self.shape = self.rotations[self.rotation]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def new_piece(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        return Tetromino(GRID_WIDTH // 2 - 1, 0, shape_index)

    def check_collision(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (
                        piece.x + x < 0
                        or piece.x + x >= GRID_WIDTH
                        or piece.y + y >= GRID_HEIGHT
                        or self.grid[piece.y + y][piece.x + x]
                    ):
                        return True
        return False

    def lock_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[piece.y + y][piece.x + x] = piece.shape_index + 1
        self.clear_lines()
        self.current_piece = self.new_piece()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = []
        for y, row in enumerate(self.grid):
            if all(row):
                lines_to_clear.append(y)

        if lines_to_clear:
            pygame.time.wait(300)  # Pause to show the completed line
            for y in lines_to_clear:
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.score += len(lines_to_clear) * 100

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))


    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[self.grid[y][x] - 1],
                        (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    )
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    1,
                )

    def draw_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        piece.color,
                        (
                            (piece.x + x) * GRID_SIZE,
                            (piece.y + y) * GRID_SIZE,
                            GRID_SIZE,
                            GRID_SIZE,
                        ),
                    )

    def run(self):
        fall_time = 0
        fall_speed = 500  # milliseconds

        while not self.game_over:
            self.screen.fill(BLACK)
            fall_time += self.clock.tick(60)

            if fall_time > fall_speed:
                fall_time = 0
                self.current_piece.y += 1
                if self.check_collision(self.current_piece):
                    self.current_piece.y -= 1
                    self.lock_piece(self.current_piece)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if self.check_collision(self.current_piece):
                            self.current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if self.check_collision(self.current_piece):
                            self.current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        if self.check_collision(self.current_piece):
                            self.current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if self.check_collision(self.current_piece):
                            self.current_piece.rotate(clockwise=False)


            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_score()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
