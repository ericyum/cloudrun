import os
import random
from flask import Flask, render_template, jsonify, send_from_directory

# Get the absolute path to the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
frontend_dir = os.path.join(basedir, '..', 'frontend')

app = Flask(__name__,
            static_folder=frontend_dir,
            static_url_path='/static', # Serve static files from /static
            template_folder=frontend_dir)

@app.route('/game_state')
def get_game_state():
    print("Game state requested!") # Debug print
    # Create a temporary board to overlay the current piece for rendering
    display_board = [row[:] for row in game_board] # Deep copy

    if not game_over and current_piece:
        for row in range(len(current_piece['shape'])):
            for col in range(len(current_piece['shape'][row])):
                if current_piece['shape'][row][col] == 1:
                    board_x = current_piece_x + col
                    board_y = current_piece_y + row
                    if board_y >= 0 and board_y < BOARD_HEIGHT and \
                       board_x >= 0 and board_x < BOARD_WIDTH:
                        display_board[board_y][board_x] = current_piece['color']

    return jsonify({
        'board': display_board,
        'current_piece': current_piece,
        'current_piece_x': current_piece_x,
        'current_piece_y': current_piece_y,
        'score': score,
        'game_over': game_over
    })

# Game constants

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetromino shapes (rotated versions will be generated)
# Each shape is a list of 4x4 matrices, representing rotations
# 0 represents empty, 1 represents a block part
# Colors are arbitrary for now, will be used for rendering
TETROMINOES = {
    'I': {'shape': [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]], 'color': 'cyan'},
    'J': {'shape': [[1,0,0], [1,1,1], [0,0,0]], 'color': 'blue'},
    'L': {'shape': [[0,0,1], [1,1,1], [0,0,0]], 'color': 'orange'},
    'O': {'shape': [[1,1], [1,1]], 'color': 'yellow'},
    'S': {'shape': [[0,1,1], [1,1,0], [0,0,0]], 'color': 'green'},
    'T': {'shape': [[0,1,0], [1,1,1], [0,0,0]], 'color': 'purple'},
    'Z': {'shape': [[1,1,0], [0,1,1], [0,0,0]], 'color': 'red'},
}

# Game state variables
# Game state variables
game_board = []
current_piece = None
current_piece_x = 0
current_piece_y = 0
score = 0
game_over = False

def create_empty_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def get_random_piece():
    shape_name = random.choice(list(TETROMINOES.keys()))
    piece_data = TETROMINOES[shape_name]
    return {
        'shape': piece_data['shape'],
        'color': piece_data['color'],
        'name': shape_name
    }

def check_collision(board, piece, x, y):
    for row in range(len(piece['shape'])):
        for col in range(len(piece['shape'][row])):
            if piece['shape'][row][col] == 1:
                board_x = x + col
                board_y = y + row
                # Check boundaries
                if board_x < 0 or board_x >= BOARD_WIDTH or \
                   board_y < 0 or board_y >= BOARD_HEIGHT:
                    return True
                # Check collision with existing blocks on the board
                if board_y >= 0 and board[board_y][board_x] != 0:
                    return True
    return False

def lock_piece():
    global game_board, current_piece, current_piece_x, current_piece_y, game_over
    for row in range(len(current_piece['shape'])):
        for col in range(len(current_piece['shape'][row])):
            if current_piece['shape'][row][col] == 1:
                board_x = current_piece_x + col
                board_y = current_piece_y + row
                if board_y < 0: # Piece locked above the board, game over
                    game_over = True
                    return
                game_board[board_y][board_x] = current_piece['color'] # Store color instead of 1

def clear_lines():
    global game_board, score
    lines_cleared = 0
    new_board = [row for row in game_board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    game_board = new_board
    score += lines_cleared * 100 # Simple scoring

def move_piece(dx, dy):
    global current_piece_x, current_piece_y, current_piece, game_over
    if game_over:
        return False

    new_x = current_piece_x + dx
    new_y = current_piece_y + dy

    if not check_collision(game_board, current_piece, new_x, new_y):
        current_piece_x = new_x
        current_piece_y = new_y
        return True
    else:
        if dy > 0: # Collision when moving down, so lock the piece
            lock_piece()
            clear_lines()
            if not game_over: # Only generate new piece if game is not over
                current_piece = get_random_piece()
                current_piece_x = BOARD_WIDTH // 2 - len(current_piece['shape'][0]) // 2
                current_piece_y = 0
                if check_collision(game_board, current_piece, current_piece_x, current_piece_y):
                    game_over = True # New piece immediately collides, game over
        return False

def rotate_piece():
    global current_piece, current_piece_x, current_piece_y
    if game_over:
        return

    original_shape = current_piece['shape']
    rotated_shape = [list(row) for row in zip(*original_shape[::-1])] # Rotate 90 degrees clockwise

    # Simple wall kick: try to move if rotation causes collision
    offsets = [(0,0), (-1,0), (1,0), (0,-1), (0,1)] # Try original, left, right, up, down
    for ox, oy in offsets:
        if not check_collision(game_board, {'shape': rotated_shape, 'color': current_piece['color']}, current_piece_x + ox, current_piece_y + oy):
            current_piece['shape'] = rotated_shape
            current_piece_x += ox
            current_piece_y += oy
            return
    # If all offsets fail, revert to original shape (no rotation)
    current_piece['shape'] = original_shape

def reset_game():
    global game_board, current_piece, current_piece_x, current_piece_y, score, game_over
    game_board = create_empty_board()
    current_piece = get_random_piece()
    current_piece_x = BOARD_WIDTH // 2 - len(current_piece['shape'][0]) // 2
    current_piece_y = 0
    score = 0
    game_over = False

# Initialize game state on startup
reset_game()

@app.route('/move/<direction>')
def handle_move(direction):
    if direction == 'left':
        move_piece(-1, 0)
    elif direction == 'right':
        move_piece(1, 0)
    elif direction == 'down':
        move_piece(0, 1)
    elif direction == 'rotate':
        rotate_piece()
    elif direction == 'reset':
        reset_game()
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    print("Flask app starting...")
    # Print all registered routes for debugging
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.endpoint} -> {rule.rule}")
    app.run(debug=True, host='0.0.0.0', port=5000)
