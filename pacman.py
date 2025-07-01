
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Ghost class
class Ghost:
    def __init__(self, x, y, color, spawn_time):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.original_color = color
        self.color = color
        self.speed = 1
        self.dx = 0
        self.dy = 0
        self.spawn_time = spawn_time # Time in frames before ghost activates
        self.state = "waiting" # "waiting", "exiting_house", "active", "frightened", "eaten"
        self.change_direction_timer = 0 # Timer to control direction changes
        self.respawn_timer = 0 # Timer for respawning after being eaten
        self.target_exit_x = 380 # Center of the ghost house exit
        self.target_exit_y = 360 # Center of the ghost house exit (adjusted for new maze)

    def draw(self, screen):
        if self.state == "frightened":
            ghost_color = (0, 0, 255) # Blue when frightened
        elif self.state == "eaten":
            ghost_color = (100, 100, 100) # Grey when eaten
        else:
            ghost_color = self.color

        # Draw the main body (inverted U shape)
        pygame.draw.arc(screen, ghost_color, (self.rect.x, self.rect.y, 40, 40), 3.14, 6.28, 20) # Top arc
        pygame.draw.rect(screen, ghost_color, (self.rect.x, self.rect.y + 20, 40, 20)) # Bottom rectangle

        # Draw the wavy bottom (triangles or circles)
        pygame.draw.circle(screen, ghost_color, (self.rect.x + 5, self.rect.y + 35), 5)
        pygame.draw.circle(screen, ghost_color, (self.rect.x + 15, self.rect.y + 38), 5)
        pygame.draw.circle(screen, ghost_color, (self.rect.x + 25, self.rect.y + 35), 5)
        pygame.draw.circle(screen, ghost_color, (self.rect.x + 35, self.rect.y + 38), 5)

        # Draw eyes (always white with black pupils)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 15, self.rect.y + 15), 5) # Left eye
        pygame.draw.circle(screen, WHITE, (self.rect.x + 25, self.rect.y + 15), 5) # Right eye
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 15, self.rect.y + 15), 2) # Left pupil
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 25, self.rect.y + 15), 2) # Right pupil

        # Draw mouth (only when not frightened or eaten)
        if self.state != "frightened" and self.state != "eaten":
            pygame.draw.line(screen, (0, 0, 0), (self.rect.x + 10, self.rect.y + 28), (self.rect.x + 15, self.rect.y + 33), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.rect.x + 15, self.rect.y + 33), (self.rect.x + 20, self.rect.y + 28), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.rect.x + 20, self.rect.y + 28), (self.rect.x + 25, self.rect.y + 33), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.rect.x + 25, self.rect.y + 33), (self.rect.x + 30, self.rect.y + 28), 2)


    def move(self):
        if self.state == "waiting":
            return
        elif self.state == "exiting_house":
            # Move towards the exit point
            if self.rect.centerx < self.target_exit_x:
                self.rect.x += self.speed
            elif self.rect.centerx > self.target_exit_x:
                self.rect.x -= self.speed
            elif self.rect.centery > self.target_exit_y:
                self.rect.y -= self.speed
            else:
                self.state = "active" # Reached exit, now active
                self.choose_new_direction() # Choose a direction outside the house

        elif self.state == "frightened":
            self.change_direction_timer += 1
            # Move at half speed when frightened
            new_x = self.rect.x + self.dx * (self.speed / 2)
            new_y = self.rect.y + self.dy * (self.speed / 2)
            temp_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

            # Always attempt to move, and if collision, choose new direction
            if not self.check_wall_collision(temp_rect):
                self.rect.x = new_x
                self.rect.y = new_y
            else:
                self.choose_new_direction()

            # Periodically choose a new direction even if not hitting a wall
            if self.change_direction_timer >= 60: # Every second (60 frames)
                self.change_direction_timer = 0
                self.choose_new_direction()

        elif self.state == "eaten":
            # Move back to ghost house
            if self.rect.centerx < self.target_exit_x:
                self.rect.x += self.speed
            elif self.rect.centerx > self.target_exit_x:
                self.rect.x -= self.speed
            elif self.rect.centery < self.target_exit_y: # Move up to the house
                self.rect.y += self.speed
            else:
                self.respawn_timer += 1
                if self.respawn_timer >= 180: # 3 seconds delay
                    self.state = "waiting" # Back in house, wait to respawn
                    self.color = self.original_color # Revert to original color
                    self.respawn_timer = 0

        elif self.state == "active":
            self.change_direction_timer += 1

            # Attempt to move
            new_x = self.rect.x + self.dx * self.speed
            new_y = self.rect.y + self.dy * self.speed
            temp_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

            if not self.check_wall_collision(temp_rect):
                self.rect.x = new_x
                self.rect.y = new_y

                # Implement wormhole effect for ghosts
                if (self.rect.centery > 160 and self.rect.centery < 200) or \
                   (self.rect.centery > 400 and self.rect.centery < 440):
                    if self.rect.centerx < 0: # If ghost goes off left edge
                        self.rect.centerx = SCREEN_WIDTH
                    elif self.rect.centerx > SCREEN_WIDTH: # If ghost goes off right edge
                        self.rect.centerx = 0
            else:
                # If hit a wall, choose a new direction immediately
                self.choose_new_direction()

            # Periodically choose a new direction even if not hitting a wall
            if self.change_direction_timer >= 60: # Every second (60 frames)
                self.change_direction_timer = 0
                self.choose_new_direction()

    def check_wall_collision(self, rect):
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == 'w':
                    wall_rect = pygame.Rect(x * 40, y * 40, 40, 40)
                    if rect.colliderect(wall_rect):
                        return True
        return False

    def choose_new_direction(self):
        valid_directions = []
        current_dx, current_dy = self.dx, self.dy

        # Only allow turns if ghost is roughly aligned with the grid
        # This prevents ghosts from turning mid-tile and getting stuck
        if self.rect.x % 40 == 0 and self.rect.y % 40 == 0:
            # Check all four directions
            all_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in all_directions:
                # Avoid reversing direction unless it's the only option
                if (dx, dy) == (-current_dx, -current_dy) and len(valid_directions) > 0:
                    continue

                temp_rect = self.rect.copy()
                temp_rect.x += dx * self.speed
                temp_rect.y += dy * self.speed

                if not self.check_wall_collision(temp_rect):
                    valid_directions.append((dx, dy))

            if valid_directions:
                # Prioritize continuing straight or turning, then reversing
                if (current_dx, current_dy) in valid_directions and random.random() < 0.8: # 80% chance to continue straight
                    self.dx, self.dy = current_dx, current_dy
                else:
                    # Filter out reversing direction if other options exist
                    non_reverse_directions = [d for d in valid_directions if d != (-current_dx, -current_dy)]
                    if non_reverse_directions:
                        self.dx, self.dy = random.choice(non_reverse_directions)
                    else:
                        self.dx, self.dy = random.choice(valid_directions) # Only reverse if no other choice
            else:
                # If completely stuck, reverse direction
                self.dx, self.dy = -current_dx, -current_dy
        else:
            # If not aligned, try to continue in current direction
            temp_rect = self.rect.copy()
            temp_rect.x += current_dx * self.speed
            temp_rect.y += current_dy * self.speed
            if not self.check_wall_collision(temp_rect):
                pass # Continue in current direction
            else:
                # If current direction is blocked, try to find any valid direction
                all_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in all_directions:
                    temp_rect = self.rect.copy()
                    temp_rect.x += dx * self.speed
                    temp_rect.y += dy * self.speed
                    if not self.check_wall_collision(temp_rect):
                        self.dx, self.dy = dx, dy
                        return



# Player class
class Player:
    def __init__(self, x, y):
        # Make the collision rect slightly smaller for forgiveness
        self.rect = pygame.Rect(x + 5, y + 5, 30, 30)
        self.direction = 0 # 0: right, 1: left, 2: up, 3: down
        self.mouth_open = True
        self.mouth_timer = 0

    def draw(self, screen):
        # Calculate the center of the original 40x40 tile
        center_x = self.rect.centerx
        center_y = self.rect.centery

        if self.mouth_open:
            # Adjust the arc drawing to be centered on the original tile
            if self.direction == 0:
                pygame.draw.arc(screen, YELLOW, (center_x - 20, center_y - 20, 40, 40), 0.5, -0.5, 20)
            elif self.direction == 1:
                pygame.draw.arc(screen, YELLOW, (center_x - 20, center_y - 20, 40, 40), 3.6, 2.6, 20)
            elif self.direction == 2:
                pygame.draw.arc(screen, YELLOW, (center_x - 20, center_y - 20, 40, 40), 2.1, 1.1, 20)
            elif self.direction == 3:
                pygame.draw.arc(screen, YELLOW, (center_x - 20, center_y - 20, 40, 40), 5.2, 4.2, 20)
        else:
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), 20)

        self.mouth_timer += 1
        if self.mouth_timer >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0

    def move(self, dx, dy):
        # Update direction based on input
        if dx > 0:
            self.direction = 0
        elif dx < 0:
            self.direction = 1
        elif dy < 0:
            self.direction = 2
        elif dy > 0:
            self.direction = 3

        # Move in X direction
        self.rect.x += dx
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == 'w':
                    wall_rect = pygame.Rect(x * 40, y * 40, 40, 40)
                    if self.rect.colliderect(wall_rect):
                        if dx > 0: # Moving right
                            self.rect.right = wall_rect.left
                        elif dx < 0: # Moving left
                            self.rect.left = wall_rect.right

        # Implement wormhole effect
        # Check if Pac-Man is in a wormhole row (rows 4 and 10)
        if (self.rect.centery > 160 and self.rect.centery < 200) or \
           (self.rect.centery > 400 and self.rect.centery < 440):
            if self.rect.centerx < 0: # If Pac-Man goes off left edge
                self.rect.centerx = SCREEN_WIDTH
            elif self.rect.centerx > SCREEN_WIDTH: # If Pac-Man goes off right edge
                self.rect.centerx = 0

        # Move in Y direction
        self.rect.y += dy
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == 'w':
                    wall_rect = pygame.Rect(x * 40, y * 40, 40, 40)
                    if self.rect.colliderect(wall_rect):
                        if dy > 0: # Moving down
                            self.rect.bottom = wall_rect.top
                        elif dy < 0: # Moving up
                            self.rect.top = wall_rect.bottom


# Pellet class
class Pellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.rect.center = (x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, 5)


# PowerPellet class
class PowerPellet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.rect.center = (x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, self.rect.center, 10)



# Maze layout
maze = [
    "wwwwwwwwwwwwwwwwwwww", # Row 0
    "wP                 P", # Row 1 - Top-left and top-right power pellets
    "w www wwww www wwww", # Row 2
    "w w   w  w w   w  w", # Row 3
    "                    ", # Row 4 - Wormhole 1 (open)
    "w www w w wwww w w w", # Row 5
    "w   w w w w  w w w w", # Row 6
    "www w w w wwww w w w", # Row 7
    "w   w   w      w   w", # Row 8 - Ghost house area
    "w www wwww www wwww", # Row 9
    "                    ", # Row 10 - Wormhole 2 (open)
    "w w   w  w w   w  w", # Row 11
    "w www wwww www wwww", # Row 12
    "P                  P", # Row 13 - Bottom-left and bottom-right power pellets
    "wwwwwwwwwwwwwwwwwwww", # Row 14
]



# Draw the maze
def draw_maze_walls(screen):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == 'w':
                pygame.draw.rect(screen, BLUE, (x * 40, y * 40, 40, 40))

# Create pellets
def create_pellets():
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == ' ':
                pellets.append(Pellet(x * 40 + 20, y * 40 + 20))
                print(f"Added Pellet at ({x*40+20}, {y*40+20})")
            elif char == 'P':
                pellets.append(PowerPellet(x * 40 + 20, y * 40 + 20))
                print(f"Added PowerPellet at ({x*40+20}, {y*40+20})")




# Game loop
player = Player(40, 40)
pellets = []
create_pellets()

ghosts = [
    Ghost(360, 200, RED, 0), # Blinky (red) - spawns immediately
    Ghost(400, 200, (0, 255, 255), 180), # Inky (cyan) - spawns after 3 seconds (180 frames)
    Ghost(440, 200, (255, 184, 255), 360), # Pinky (pink) - spawns after 6 seconds
    Ghost(480, 200, (255, 184, 82), 540) # Clyde (orange) - spawns after 9 seconds
]

clock = pygame.time.Clock()
FPS = 60

game_time = 0 # Keep track of game time in frames
frightened_timer = 0 # Timer for frightened ghost state
score = 0 # Game score
print(f"Initial score: {score}")

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-2, 0)
    if keys[pygame.K_RIGHT]:
        player.move(2, 0)
    if keys[pygame.K_UP]:
        player.move(0, -2)
    if keys[pygame.K_DOWN]:
        player.move(0, 2)

    # Check for collisions with pellets
    for pellet in pellets:
        if player.rect.colliderect(pellet.rect):
            if isinstance(pellet, PowerPellet):
                for ghost in ghosts:
                    if ghost.state == "active":
                        ghost.state = "frightened"
                # Start frightened timer
                frightened_timer = 360 # 6 seconds
                score += 50 # Power pellet score
            else:
                score += 10 # Regular pellet score
            pellets.remove(pellet)

    # Update frightened timer
    if frightened_timer > 0:
        frightened_timer -= 1
        if frightened_timer == 0:
            for ghost in ghosts:
                if ghost.state == "frightened":
                    ghost.state = "active"

    # Update game time
    game_time += 1

    # Activate ghosts based on spawn time
    for ghost in ghosts:
        if ghost.state == "waiting" and game_time >= ghost.spawn_time:
            ghost.state = "exiting_house"

    # Move the ghosts
    for ghost in ghosts:
        ghost.move()

    # Check for collisions between player and ghosts
    for ghost in ghosts:
        if player.rect.colliderect(ghost.rect):
            if ghost.state == "frightened":
                ghost.state = "eaten"
                ghost.rect.x = 360 # Send back to ghost house
                ghost.rect.y = 200
                score += 200 # Score for eating a ghost
            elif ghost.state == "active":
                game_over = True

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000) # Wait for 3 seconds
        running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw the maze
    draw_maze_walls(screen)

    # Draw the player
    player.draw(screen)

    # Draw the pellets
    for pellet in pellets:
        pellet.draw(screen)

    # Draw the ghosts
    for ghost in ghosts:
        ghost.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (5, 5))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
