import pygame as p
import time

# Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 850
FPS = 60
FONT_SIZE = 75
STATE_FONT_SIZE = 45
SLIDE_DURATION = 0.5
DELAY = 0.5
TAPE_SHIFT = -0.5
BG_COLOR = (12, 12, 12)
TAPE_TXT_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
HIGHLIGHT_COLOR = (255, 0, 0)
TAPE_LENGTH = 6
INITIAL_TAPE = [0] * TAPE_LENGTH
INITIAL_HEAD_POSITION = TAPE_LENGTH // 2

# Turing Machine Logic
TURING_MACHINE_CODE = {
    'q0': {
        0: ('q1', 1, 1),
        1: ('H', 1, 1),
    },
    'q1': {
        0: ('q2', 0, 1),
        1: ('q1', 1, 1),
    },
    'q2': {
        0: ('q2', 1, -1),
        1: ('q0', 1, -1),
    },
    'H': {
        0: ('H', 0, 0),
        1: ('H', 1, 0),
    },
}

class TuringMachine:
    def __init__(self, tape, head_position, transitions):
        self.tape = tape
        self.head_position = head_position
        self.transitions = transitions
        self.current_state = 'q0'

    def step(self):
        if self.current_state == 'H':
            return False
        if self.head_position < 0:
            self.tape.insert(0, 0)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(0)
        current_value = self.tape[self.head_position]
        next_state, write_value, move_direction = self.transitions[self.current_state][current_value]
        self.tape[self.head_position] = write_value
        self.head_position += move_direction
        self.current_state = next_state
        return True

def draw_tape(screen, font, tape, center_index, offset_x=0):
    cell_width = WINDOW_WIDTH // 10
    total_offset = (TAPE_SHIFT * cell_width) + offset_x
    start_index = max(0, center_index - 5)
    end_index = min(len(tape), center_index + 6)
    for i, tape_index in enumerate(range(start_index, end_index)):
        x = i * cell_width + (WINDOW_WIDTH // 2 - 5 * cell_width) + total_offset
        value = tape[tape_index]
        rect = p.draw.rect(screen, WHITE, (x, WINDOW_HEIGHT // 2 - 50, cell_width, 100))
        p.draw.rect(screen, BG_COLOR, rect, 2)
        text = font.render(str(value), True, TAPE_TXT_COLOR)
        screen.blit(text, (x + cell_width // 2 - text.get_width() // 2,
                           WINDOW_HEIGHT // 2 - 50 + 50 - text.get_height() // 2))
    highlight_x = WINDOW_WIDTH // 2 - cell_width // 2
    highlight_rect = p.Rect(highlight_x, WINDOW_HEIGHT // 2 - 50, cell_width, 100)
    p.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 5)

def draw_state(screen, font, state):
    text = font.render(f"State: {state}", True, BLUE)
    bg_rect = p.Rect(WINDOW_WIDTH // 2 - text.get_width() // 2 - 10, 10,
                     text.get_width() + 20, text.get_height() + 10)
    p.draw.rect(screen, WHITE, bg_rect)
    screen.blit(text, (bg_rect.x + 10, bg_rect.y + 5))

def animate_slide(screen, font, tape, center_index, direction, duration):
    if direction == 0:
        return
    cell_width = WINDOW_WIDTH // 10
    total_offset = direction * cell_width
    frames = int(duration * FPS)
    for frame in range(frames):
        offset_x = total_offset * (frame / frames)
        screen.fill(BG_COLOR)
        draw_tape(screen, font, tape, center_index, -offset_x)
        p.display.flip()
        p.time.Clock().tick(FPS)

def main():
    p.init()
    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    p.display.set_caption("Turing Machine Simulation")
    font = p.font.SysFont(None, FONT_SIZE)
    stat_font = p.font.SysFont(None, STATE_FONT_SIZE)

    tape = INITIAL_TAPE[:]
    head_position = INITIAL_HEAD_POSITION
    turing_machine = TuringMachine(tape, head_position, TURING_MACHINE_CODE)

    running = True
    working = True
    delay = DELAY

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        old_head_position = turing_machine.head_position
        if working:
            working = turing_machine.step()
        direction = turing_machine.head_position - old_head_position

        animate_slide(screen, font, turing_machine.tape, old_head_position, direction, SLIDE_DURATION)
        screen.fill(BG_COLOR)
        draw_tape(screen, font, turing_machine.tape, turing_machine.head_position)
        draw_state(screen, stat_font, turing_machine.current_state)
        p.display.flip()
        time.sleep(delay)

    p.quit()

if __name__ == "__main__":
    main()