import pygame
import random
import json
import os

# Dimensions
width, height = 900, 600
snakeUnit = 15

# Initialize game
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
cyan = (0, 255, 255)
red = (255, 0, 0)
green = (34, 139, 34)


# Prints message on screen
def message(msg, size, colour, cw, ch):
    mesg = pygame.font.Font('freesansbold.ttf', size).render(msg, True, colour)
    msgRect = mesg.get_rect()
    msgRect.center = (cw, ch)
    screen.blit(mesg, msgRect)

game_close = False
while not game_close:
    # Menu loop
    screen.fill(black)
    game_over = True
    while not game_close and game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close Window
                game_close = True
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameSpeed = 5
                    game_over = False
                elif event.key == pygame.K_2:
                    gameSpeed = 10
                    game_over = False
                elif event.key == pygame.K_3:
                    gameSpeed = 15
                    game_over = False
                elif event.key == pygame.K_4:
                    gameSpeed = 20
                    game_over = False
        message("Select Difficulty", 50, white, width // 2, height // 2)
        message("Press 1: Easy    Press 2: Medium    Press 3: Hard    Press 4: Master", 25, red, width // 2,
                5 * height // 8)
        pygame.display.update()

    # Initialize Game Variables
    clock = pygame.time.Clock()
    x, y = width // 2, height // 2
    dx, dy = 0, 0
    food_x, food_y = random.randrange(0, width, snakeUnit), random.randrange(0, height, snakeUnit)
    snakeLength = 1
    snake = [[x, y]]
    if os.path.exists('highscore.json'):
        with open('highscore.json', 'r') as f:
            highScore = json.load(f)['hs']
    else:
        highScore = 0

    # Game Loop
    while not game_close and not game_over:
        # Movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close Window
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and dx <= 0:
                    dx = -snakeUnit
                    dy = 0
                elif event.key == pygame.K_d and dx >= 0:
                    dx = snakeUnit
                    dy = 0
                elif event.key == pygame.K_w and dy <= 0:
                    dy = -snakeUnit
                    dx = 0
                elif event.key == pygame.K_s and dy >= 0:
                    dy = snakeUnit
                    dx = 0
        x += dx
        y += dy
        # Out of Bounds
        if x + snakeUnit > width or x < 0 or y + snakeUnit > height or y < 0:
            game_over = True
        # Eat Food
        if x == food_x and y == food_y:
            snakeLength += random.randint(2, 5)
            while True:
                food_x, food_y = random.randrange(0, width, snakeUnit), random.randrange(0, height, snakeUnit)
                if [food_x, food_y] not in snake and food_x != x and food_y != y:
                    break
        # Tail Death
        if [x, y] in snake and len(snake) > 1:
            game_over = True
        # Manage Snake Length
        snake.append([x, y])
        if len(snake) > snakeLength:
            del snake[0]

        # Draw Objects
        screen.fill(white)
        for s in snake:
            pygame.draw.rect(screen, green, [s[0], s[1], snakeUnit, snakeUnit])
        pygame.draw.rect(screen, red, [food_x, food_y, snakeUnit, snakeUnit])
        message("Score: {}".format(snakeLength-1), 20, cyan, 50, 20)
        message("High Score: {}".format(highScore), 20, cyan, 80, 50)
        if snakeLength-1 > highScore:
            highScore = snakeLength - 1

        # Refresh Game
        pygame.display.update()
        clock.tick(gameSpeed)

    if not game_close:
        # Losing Screen
        screen.fill(white)
        message("You lost", 50, red, width // 2, height // 2)
        pygame.display.update()
        pygame.time.delay(1000)
        message("Your score was: {}".format(snakeLength-1), 25, red, width // 2, 5 * height // 8)
        pygame.display.update()
        pygame.time.delay(1000)
        message("Press Q to quit or R to restart.", 25, red, width // 2, 7 * height // 8)
        pygame.display.update()
        while not game_close and game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close Window
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                    elif event.key == pygame.K_r:
                        game_over = False
    with open('highscore.json', 'w') as f:
        json.dump({'hs': highScore}, f)
pygame.quit()
