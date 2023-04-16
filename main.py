import pygame
import numpy as np
import pygame.mixer

# Initialize the mixer module
pygame.mixer.init()

# Load the background music file
pygame.mixer.music.load("background_music.wav")

# Set the volume (optional)
pygame.mixer.music.set_volume(0.5)

# Play the music in a loop
pygame.mixer.music.play(-1)

pygame.init()


# Set up the window dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddles
paddle_width = 10
paddle_height = 100
player_paddle_x = 20
player_paddle_y = (screen_height - paddle_height) // 2
opponent_paddle_x = screen_width - paddle_width - 20
opponent_paddle_y = (screen_height - paddle_height) // 2
paddle_speed = 5

# Ball
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball_speed_increase = 1.005


# Score
player_score = 0
opponent_score = 0  


def play_sound(frequency, duration, volume):
    """Plays a sine wave at the specified frequency and duration with specified volume"""
    sample_rate = 44100  # CD-quality sample rate in Hz
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    wave *= volume  # adjust volume
    wave = np.repeat(wave, 2)  # repeat the wave for both channels
    wave = wave.reshape(-1, 2)  # reshape the array to have two dimensions
    normalized_wave = np.int16(wave * (2 ** 15 - 1))
    sound = pygame.sndarray.make_sound(normalized_wave)
    sound.play()


# Function to reset the ball to the center of the screen
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 5
    ball_speed_y = 5

def calculate_opponent_racket_position():
    # Move the opponent racket based on the ball's position, only if the ball is moving towards the opponent's side
    global opponent_paddle_y, ball_speed_x, ball_y, paddle_height
    if ball_speed_x > 0:
        if opponent_paddle_y + paddle_height // 2 < ball_y:
            opponent_paddle_y += 5
        elif opponent_paddle_y + paddle_height // 2 > ball_y:
            opponent_paddle_y -= 5


def calculate_ball_collision():
    # Check for collisions with the top and bottom walls
    global ball_speed_y, ball_speed_x, player_score, opponent_score, ball_speed_increase, ball_y, ball_x
    if ball_y - ball_radius < 0:
        ball_y = ball_radius
        ball_speed_y = abs(ball_speed_y) * ball_speed_increase
        play_sound(100, 0.05, 0.5)
    elif ball_y + ball_radius > screen_height:
        ball_y = screen_height - ball_radius
        ball_speed_y = -abs(ball_speed_y) * ball_speed_increase
        play_sound(100, 0.05, 0.5)

    # Check for collisions with the player and opponent paddles
    if (ball_x - ball_radius <= player_paddle_x + paddle_width and
        ball_y >= player_paddle_y and
        ball_y <= player_paddle_y + paddle_height):
        ball_speed_x = -ball_speed_x
        ball_speed_x *= ball_speed_increase
        ball_speed_y *= ball_speed_increase
        play_sound(100, 0.05, 0.5)
    elif (ball_x + ball_radius >= opponent_paddle_x and
        ball_y >= opponent_paddle_y and
        ball_y <= opponent_paddle_y + paddle_height):
        ball_speed_x = -ball_speed_x
        ball_speed_x *= ball_speed_increase
        ball_speed_y *= ball_speed_increase       
        play_sound(100, 0.05, 0.5)

    # Check if the ball went past the left or right edge of the screen
    if ball_x < 0:
        opponent_score += 1
        reset_ball()
    if ball_x > screen_width:
        player_score += 1
        reset_ball()


def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))

def draw_ball(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), ball_radius)

def draw_score():
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(str(player_score), True, WHITE)
    opponent_score_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_score_text, (screen_width // 4, 10))
    screen.blit(opponent_score_text, (3 * screen_width // 4, 10))

clock = pygame.time.Clock()
game_over = False

# Define font for the menu
font = pygame.font.Font(None, 50)

# Create the menu options
start_text = font.render("Start game", True, WHITE)
start_rect = start_text.get_rect(center=(screen_width//2, screen_height//2 - 50))
quit_text = font.render("Quit", True, WHITE)
quit_rect = quit_text.get_rect(center=(screen_width//2, screen_height//2 + 50))

# Loop until the user selects an option
menu_loop = True
while menu_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_loop = False
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                menu_loop = False
                # Add a countdown before starting the game
                count_down_texts = [font.render("3", True, WHITE),
                                    font.render("2", True, WHITE),
                                    font.render("1", True, WHITE)]
                for text in count_down_texts:
                    screen.fill(BLACK)
                    screen.blit(text, text.get_rect(center=(screen_width // 2, screen_height // 2)))
                    pygame.display.update()
                    pygame.time.wait(1000)
            elif quit_rect.collidepoint(mouse_pos):
                menu_loop = False
                game_over = True

    # Draw the menu options
    screen.fill(BLACK)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.update()
    clock.tick(60)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_paddle_y = max(player_paddle_y - paddle_speed, 0)
    if keys[pygame.K_s]:
        player_paddle_y = min(player_paddle_y + paddle_speed, screen_height - paddle_height)

    screen.fill(BLACK)
    draw_paddle(player_paddle_x, player_paddle_y)
    draw_paddle(opponent_paddle_x, opponent_paddle_y)
    draw_ball(ball_x, ball_y)
    draw_score()
    # Draw a white line in the middle of the screen to resemble a tennis net
    pygame.draw.line(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)

    # Update the game
    # Update the ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    calculate_ball_collision()
    calculate_opponent_racket_position()
    # Render the game

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()

