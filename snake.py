import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake properties
snake_block = 20
snake_speed = 10

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, white, [segment[0], segment[1], snake_block, snake_block])
    # Draw eyes on the head
    if len(snake_list) > 0:
        head = snake_list[-1]
        eye_size = snake_block // 5
        eye_offset = snake_block // 4
        # A simple representation of eyes
        pygame.draw.rect(screen, black, [head[0] + eye_offset, head[1] + eye_offset, eye_size, eye_size])
        pygame.draw.rect(screen, black, [head[0] + snake_block - eye_offset * 2, head[1] + eye_offset, eye_size, eye_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    # Snake initial position
    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, screen_width - snake_block) / float(snake_block)) * float(snake_block)
    foody = round(random.randrange(0, screen_height - snake_block) / float(snake_block)) * float(snake_block)

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            screen.fill(white)
            message("Game Over! Q-Quit, C-Play", red)
            show_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / float(snake_block)) * float(snake_block)
            foody = round(random.randrange(0, screen_height - snake_block) / float(snake_block)) * float(snake_block)
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
