const gameBoardElement = document.getElementById('game-board');
const scoreElement = document.getElementById('score');

const BOARD_WIDTH = 10;
const BOARD_HEIGHT = 20;
const CELL_SIZE = 20; // pixels

let gameInterval;

function createBoardCells() {
    for (let i = 0; i < BOARD_WIDTH * BOARD_HEIGHT; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        gameBoardElement.appendChild(cell);
    }
}

function drawBoard(board) {
    const cells = gameBoardElement.children;
    for (let y = 0; y < BOARD_HEIGHT; y++) {
        for (let x = 0; x < BOARD_WIDTH; x++) {
            const cellIndex = y * BOARD_WIDTH + x;
            const cell = cells[cellIndex];
            // Clear previous block classes and colors
            cell.classList.remove('block');
            cell.style.backgroundColor = '';

            if (board[y][x] !== 0) {
                cell.classList.add('block');
                cell.style.backgroundColor = board[y][x]; // Use color from backend
            }
        }
    }
}

// No longer need drawPiece as backend sends overlaid board

async function sendMove(direction) {
    try {
        await fetch(`/move/${direction}`);
        fetchGameState(); // Refresh game state after move
    } catch (error) {
        console.error(`Error sending move ${direction}:`, error);
    }
}

async function fetchGameState() {
    try {
        const response = await fetch('/game_state');
        const data = await response.json();

        drawBoard(data.board);
        scoreElement.textContent = `Score: ${data.score}`;

        if (data.game_over) {
            clearInterval(gameInterval);
            console.log("Game Over!");
            alert(`Game Over! Your score: ${data.score}. Press 'R' to restart.`);
        }

    } catch (error) {
        console.error('Error fetching game state:', error);
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        sendMove('left');
    } else if (e.key === 'ArrowRight') {
        sendMove('right');
    } else if (e.key === 'ArrowDown') {
        sendMove('down');
    } else if (e.key === 'ArrowUp') { // Rotate with Up arrow
        sendMove('rotate');
    } else if (e.key === 'r' || e.key === 'R') { // Reset game with 'R' key
        sendMove('reset');
        // Restart game interval after reset
        clearInterval(gameInterval);
        gameInterval = setInterval(() => sendMove('down'), 500); // Block falls every 500ms
    }
});

// Initialize board cells once
createBoardCells();

// Start game loop: block falls every 500ms
gameInterval = setInterval(() => sendMove('down'), 500);

// Initial fetch of game state
fetchGameState();

console.log("Tetris script loaded!");
