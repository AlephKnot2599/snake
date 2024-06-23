import os
import random
import sys

import pygame

# Game settings
WIDTH, HEIGHT = 640, 480
SNAKE_SIZE = 20
FPS = 10

# Colors
GREEN = (0, 195, 10)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0
paused = False
font = pygame.font.SysFont("Arial", 24)
title = font.render("Snek", True, (255, 255, 255))

# Game state
snake = [(WIDTH // 2, HEIGHT // 2)]
food = (
    random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
    random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE,
)
direction = (0, -SNAKE_SIZE)


def draw_snake():
    for position in snake:
        pygame.draw.rect(
            screen, GREEN, pygame.Rect(position[0], position[1], SNAKE_SIZE, SNAKE_SIZE)
        )


def draw_food():
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))


def update_snake():
    global food
    snake.insert(0, (snake[0][0] + direction[0], snake[0][1] + direction[1]))
    if snake[0] == food:
        food = (
            random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
            random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE,
        )
    else:
        snake.pop()


def is_game_over():
    return (
        snake[0][0] < 0
        or snake[0][1] < 0
        or snake[0][0] >= WIDTH
        or snake[0][1] >= HEIGHT
        or snake[0] in snake[1:]
    )


def restart_game():
    global snake, food, direction
    snake = [(WIDTH // 2, HEIGHT // 2)]
    food = (
        random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
        random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE,
    )
    direction = (0, -SNAKE_SIZE)


def game_over_menu():
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to play again", True, (255, 255, 255))
    quit_text = font.render("Press Q to quit", True, (255, 255, 255))

    game_over_x = (WIDTH - game_over_text.get_width()) // 2
    score_x = (WIDTH - score_text.get_width()) // 2
    restart_x = (WIDTH - restart_text.get_width()) // 2
    quit_x = (WIDTH - quit_text.get_width()) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (game_over_x, HEIGHT // 2 - 40))
        screen.blit(score_text, (score_x, HEIGHT // 2))
        screen.blit(restart_text, (restart_x, HEIGHT // 2 + 40))
        screen.blit(quit_text, (quit_x, HEIGHT // 2 + 80))
        pygame.display.flip()
        clock.tick(FPS)


# Outer game loop
while True:
    # Reset the game state
    restart_game()

    # Inner game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_UP and direction != (0, SNAKE_SIZE):
                    direction = (0, -SNAKE_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -SNAKE_SIZE):
                    direction = (0, SNAKE_SIZE)
                elif event.key == pygame.K_LEFT and direction != (SNAKE_SIZE, 0):
                    direction = (-SNAKE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-SNAKE_SIZE, 0):
                    direction = (SNAKE_SIZE, 0)

        if paused:
            continue

        screen.fill((0, 0, 0))

        # Calculate the position of the title
        title_width = title.get_width()
        title_height = title.get_height()
        title_x = (WIDTH - title_width) // 2
        title_y = 10  # 10 pixels from the top

        # Display the title
        screen.blit(title, (title_x, title_y))

        draw_snake()
        draw_food()

        update_snake()

        if is_game_over():
            game_over_menu()
            break

        score = len(snake) - 1

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
