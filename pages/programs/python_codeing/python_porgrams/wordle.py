import pygame
import random

pygame.init()

# Set up display
width, height = 1600, 837
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wordle")

# Set up fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 40)

# Set up colors
BG_color = (250, 250, 250)
txt_col = (32, 32, 32)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
red = (255, 0, 0)

# List of words
word_list = ["rocks", "numpy", "sussy", "updog", "sigma", "mugus", "elips", "shift", "memes", "check", "wrong",
             "green", "viral", "water", "while"]

square_size = 74
square_padding = 10
max_guesses = 6

def calculate_grid_position(word_len):
    grid_width = word_len * (square_size + square_padding) - square_padding
    grid_height = max_guesses * (square_size + square_padding) - square_padding
    return (width - grid_width) // 2, (height - grid_height) // 2

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def check_guess(guess, word):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == word[i]:
            feedback.append(green)
        elif guess[i] in word:
            feedback.append(yellow)
        else:
            feedback.append(gray)
    return feedback

def restart():
    global word, grid_x, grid_y, guesses, input_text, error_message, error_timer, feedback_dict
    word = random.choice(word_list).upper()
    grid_x, grid_y = calculate_grid_position(len(word))
    guesses = []
    input_text = ""
    error_message = ""
    error_timer = 0
    feedback_dict = {}

word = random.choice(word_list).upper()
grid_x, grid_y = calculate_grid_position(len(word))
guesses = []
input_text = ""
error_message = ""
error_timer = 0
feedback_dict = {}

running = True
while running:
    win.fill(BG_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(input_text) == len(word):
                    if input_text.upper() in [w.upper() for w in word_list]:
                        feedback = check_guess(input_text.upper(), word)
                        guesses.append((input_text.upper(), feedback))
                        input_text = ""
                        error_message = ""
                        for i, char in enumerate(guesses[-1][0]):
                            feedback_dict[char] = feedback[i]
                    else:
                        error_message = f"'{input_text.upper()}' is not in the word list."
                        error_timer = 180
                else:
                    error_message = "Word length mismatch!"
                    error_timer = 180
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif len(input_text) < len(word) and event.unicode.isalpha():
                input_text += event.unicode.upper()
            elif event.key == pygame.K_r:
                restart()
    
    # Draw the guesses and feedback
    for i, (guess, feedback) in enumerate(guesses):
        for j, char in enumerate(guess):
            x = grid_x + j * (square_size + square_padding)
            y = grid_y + i * (square_size + square_padding)
            pygame.draw.rect(win, feedback[j], (x, y, square_size, square_size))
            draw_text(char, font, txt_col, win, x + square_size // 2, y + square_size // 2)

    # Draw the current input text
    for j, char in enumerate(input_text):
        x = grid_x + j * (square_size + square_padding)
        y = grid_y + len(guesses) * (square_size + square_padding)
        pygame.draw.rect(win, txt_col, (x, y, square_size, square_size), 2)
        draw_text(char, font, txt_col, win, x + square_size // 2, y + square_size // 2)
    
    # Error message for invalid guess or word length mismatch
    if error_message:
        if error_timer > 0:
            error_timer -= 1
            draw_text(error_message, small_font, red, win, width // 2, height - 50)
        else:
            error_message = ""

    # Check if the game is over
    if len(guesses) >= max_guesses or (guesses and guesses[-1][0] == word):
        if guesses[-1][0] == word:
            draw_text("You Won!", font, red, win, width // 2, height // 2)
        else:
            draw_text("Game Over!", font, red, win, width // 2, height // 2)
        draw_text(f"The word was {word}", small_font, red, win, width // 2, height // 2 + 60)

    pygame.display.flip()

pygame.quit()