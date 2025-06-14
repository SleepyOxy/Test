import pygame
import random
from pygame.locals import QUIT
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5
BALL_SIZE = 10
BALL_SPEED_BASE = 2
WINNING_SCORE = 10


FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

player1_x = 50
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_x = WIDTH - 50 - PADDLE_WIDTH
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_speed_x = BALL_SPEED_BASE * random.choice((1, -1))
ball_speed_y = BALL_SPEED_BASE * random.choice((1, -1))


player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)


game_state = "playing" 

def display_message(message, color):
    screen.fill(BLACK)
    text = font.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Show message for 3 seconds

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH // 2 - BALL_SIZE // 2
    ball_y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed_x = BALL_SPEED_BASE * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_BASE * random.choice((1, -1))




# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
            player1_y += PADDLE_SPEED
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
            player2_y += PADDLE_SPEED

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y *= -1

        if (player1_x <= ball_x <= player1_x + PADDLE_WIDTH and
            player1_y <= ball_y <= player1_y + PADDLE_HEIGHT):
            ball_speed_x *= -1
        if (player2_x <= ball_x <= player2_x + PADDLE_WIDTH and
            player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
            ball_speed_x *= -1

        if ball_x < 0:
            player2_score += 1
            reset_ball()

        if ball_x > WIDTH:
            player1_score += 1
            reset_ball()

        if player1_score >= WINNING_SCORE:
            display_message("Player 1 Wins!", GREEN)
            game_state = "win"
            running = False
        elif player2_score >= WINNING_SCORE:
            display_message("Player 2 Wins!", RED)
            game_state = "lose"
            running = False

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
        score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
        pygame.display.flip()

        clock.tick(FPS)  # Use the defined FPS

    elif game_state in ("win", "lose"):
        pass

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False  
pygame.quit()