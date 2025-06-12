import pygame as p
p.init()

WIDTH, HEIGHT = 1600, 837
WIN = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Connect 4")
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
PLAYER_1_COLOR = (255, 0, 0)
PLAYER_2_COLOR = (0, 0, 255)
EMPTY_COLOR = (255, 255, 255)
GRID_ROWS = 6
GRID_COLS = 7
SQUARE_SIZE = 118
GRID_WIDTH = GRID_COLS * SQUARE_SIZE
GRID_HEIGHT = GRID_ROWS * SQUARE_SIZE
OFFSET_X = (WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2
board = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
transposition_table = {}

def draw_board():
    WIN.fill(BACKGROUND_COLOR)
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = OFFSET_X + col * SQUARE_SIZE
            y = OFFSET_Y + row * SQUARE_SIZE
            p.draw.rect(WIN, GRID_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            color = EMPTY_COLOR
            if board[row][col] == 1:
                color = PLAYER_1_COLOR
            elif board[row][col] == 2:
                color = PLAYER_2_COLOR
            p.draw.circle(WIN, color, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 7)
    p.display.flip()

def animate_disc_fall(row, col, player):
    x = OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
    target_y = OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
    current_y = OFFSET_Y
    velocity = 0
    acceleration = 0.2
    while current_y < target_y:
        velocity += acceleration
        current_y += velocity
        if current_y > target_y:
            current_y = target_y
        draw_board()
        p.draw.circle(WIN, PLAYER_1_COLOR if player == 1 else PLAYER_2_COLOR, (x, int(current_y)), SQUARE_SIZE // 2 - 7)
        p.display.flip()
        p.time.delay(10)

def is_valid_column(col):
    return 0 <= col < GRID_COLS and board[0][col] == 0

def drop_disc(col, player):
    for row in range(GRID_ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row, col
    return None, None

def undo_disc(row, col):
    board[row][col] = 0

def check_win(player):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for col in range(GRID_COLS):
        for row in range(GRID_ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(GRID_ROWS - 3):
        for col in range(GRID_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, GRID_ROWS):
        for col in range(GRID_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def evaluate_window(window, player):
    score = 0
    opponent = 3 - player
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 5
    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 80
    return score

def score_position(player):
    score = 0
    center_array = [board[row][GRID_COLS // 2] for row in range(GRID_ROWS)]
    center_count = center_array.count(player)
    score += center_count * 6

    for row in range(GRID_ROWS):
        row_array = [board[row][col] for col in range(GRID_COLS)]
        for col in range(GRID_COLS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player)

    for col in range(GRID_COLS):
        col_array = [board[row][col] for row in range(GRID_ROWS)]
        for row in range(GRID_ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player)

    for row in range(GRID_ROWS - 3):
        for col in range(GRID_COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    for row in range(3, GRID_ROWS):
        for col in range(GRID_COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)
    return score

def get_valid_columns():
    return [col for col in range(GRID_COLS) if is_valid_column(col)]

def is_terminal_node():
    return check_win(1) or check_win(2) or len(get_valid_columns()) == 0

def board_hash():
    return tuple(tuple(row) for row in board)

def minimax(depth, alpha, beta, maximizing_player):
    hashed_board = board_hash()
    if hashed_board in transposition_table:
        return transposition_table[hashed_board]

    valid_columns = get_valid_columns()
    terminal = is_terminal_node()

    if depth == 0 or terminal:
        if terminal:
            if check_win(2):
                return None, float('inf')
            elif check_win(1):
                return None, float('-inf')
            else:
                return None, 0
        else:
            return None, score_position(2)

    if maximizing_player:
        value = float('-inf')
        best_col = None
        for col in valid_columns:
            move = drop_disc(col, 2)
            if move is None:
                continue
            row, _ = move
            new_score = minimax(depth - 1, alpha, beta, False)[1]
            undo_disc(row, col)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        transposition_table[hashed_board] = (best_col, value)
        return best_col, value
    else:
        value = float('inf')
        best_col = None
        for col in valid_columns:
            move = drop_disc(col, 1)
            if move is None:
                continue
            row, _ = move
            new_score = minimax(depth - 1, alpha, beta, True)[1]
            undo_disc(row, col)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        transposition_table[hashed_board] = (best_col, value)
        return best_col, value

def game_loop():
    current_player = 1
    running = True
    while running:
        draw_board()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.MOUSEBUTTONDOWN and current_player == 1:
                x_pos = event.pos[0]
                col = (x_pos - OFFSET_X) // SQUARE_SIZE
                row, col = drop_disc(col, current_player)
                if row is not None and col is not None:
                    animate_disc_fall(row, col, current_player)
                    if check_win(current_player):
                        print(f"Player {current_player} wins!")
                        running = False
                    current_player = 2
                else:
                    print("Column is full, try again!")
        if current_player == 2:
            best_col, _ = minimax(7, float('-inf'), float('inf'), True)
            if best_col is not None:
                row, _ = drop_disc(best_col, current_player)
                if row is not None:
                    animate_disc_fall(row, best_col, current_player)
                    if check_win(current_player):
                        print(f"Player {current_player} wins!")
                        running = False
                current_player = 1
            else:
                return
                running = False
        p.time.delay(500)
    p.quit()

game_loop()