
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game objects
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
player1 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 70, 10, 140)
player2 = pygame.Rect(10, HEIGHT // 2 - 70, 10, 140)

# Game variables
ball_speed_x = 7
ball_speed_y = 7
player1_speed = 0
player2_speed = 7
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball_speed_y *= -1
    ball_speed_x *= -1

def main():
    global ball_speed_x, ball_speed_y, player1_speed, player1_score, player2_score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player1_speed += 7
                if event.key == pygame.K_UP:
                    player1_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player1_speed -= 7
                if event.key == pygame.K_UP:
                    player1_speed += 7

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0:
            player1_score += 1
            ball_restart()
        if ball.right >= WIDTH:
            player2_score += 1
            ball_restart()

        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Player movement
        player1.y += player1_speed
        if player1.top <= 0:
            player1.top = 0
        if player1.bottom >= HEIGHT:
            player1.bottom = HEIGHT

        if player2.top < ball.y:
            player2.top += player2_speed
        if player2.bottom > ball.y:
            player2.bottom -= player2_speed
        if player2.top <= 0:
            player2.top = 0
        if player2.bottom >= HEIGHT:
            player2.bottom = HEIGHT

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        player1_text = font.render(f"{player1_score}", True, WHITE)
        screen.blit(player1_text, (WIDTH / 2 + 20, 10))

        player2_text = font.render(f"{player2_score}", True, WHITE)
        screen.blit(player2_text, (WIDTH / 2 - 45, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main()
