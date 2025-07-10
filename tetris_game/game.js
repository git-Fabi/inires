// Game board configuration
const boardWidth = 10;
const boardHeight = 20;
let board = Array.from({ length: boardHeight }, () => Array(boardWidth).fill(0));

// Tetromino shapes
const tetrominoes = {
    I: [[1, 1, 1, 1]],
    O: [[1, 1], [1, 1]],
    T: [[0, 1, 0], [1, 1, 1]],
    J: [[1, 0, 0], [1, 1, 1]],
    L: [[0, 0, 1], [1, 1, 1]],
    S: [[0, 1, 1], [1, 1, 0]],
    Z: [[1, 1, 0], [0, 1, 1]]
};

let currentTetromino;
let currentPosition;
let score = 0;

// Sound effects
const dropSound = new Audio('sounds/drop.mp3');
const clearSound = new Audio('sounds/clear.mp3');
const levelUpSound = new Audio('sounds/level-up.mp3');
const gameOverSound = new Audio('sounds/game-over.mp3');

// Function to draw the game board
function drawBoard() {
    const gameBoard = document.getElementById('game-board');
    gameBoard.innerHTML = '';
    board.forEach(row => {
        const rowDiv = document.createElement('div');
        row.forEach(cell => {
            const cellDiv = document.createElement('div');
            cellDiv.className = cell ? 'filled' : 'empty';
            rowDiv.appendChild(cellDiv);
        });
        gameBoard.appendChild(rowDiv);
    });
}

// Function to generate a random tetromino
function generateTetromino() {
    const tetrominoKeys = Object.keys(tetrominoes);
    const randomKey = tetrominoKeys[Math.floor(Math.random() * tetrominoKeys.length)];
    currentTetromino = tetrominoes[randomKey];
    currentPosition = { x: Math.floor(boardWidth / 2) - 1, y: 0 }; // Start at the top center
}

// Function to draw the current tetromino
function drawTetromino() {
    currentTetromino.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            if (cell) {
                board[currentPosition.y + rowIndex][currentPosition.x + colIndex] = cell;
            }
        });
    });
}

// Function to move the tetromino down
function moveTetromino() {
    currentPosition.y++;
    if (collision()) {
        currentPosition.y--;
        drawTetromino();
        dropSound.play(); // Play drop sound
        generateTetromino();
    }
}

// Function to rotate the tetromino
function rotateTetromino() {
    const rotated = currentTetromino[0].map((_, index) => currentTetromino.map(row => row[index]).reverse());
    const originalTetromino = currentTetromino;
    currentTetromino = rotated;
    if (collision()) {
        currentTetromino = originalTetromino; // Revert if collision occurs
    }
}

// Function to check for collisions
function collision() {
    return currentTetromino.some((row, rowIndex) => {
        return row.some((cell, colIndex) => {
            if (cell) {
                const newX = currentPosition.x + colIndex;
                const newY = currentPosition.y + rowIndex;
                return newX < 0 || newX >= boardWidth || newY >= boardHeight || board[newY] && board[newY][newX];
            }
            return false;
        });
    });
}

// Game loop
function gameLoop() {
    moveTetromino();
    drawBoard();
    setTimeout(gameLoop, 1000); // Repeat every second
}

// Event listeners for controls
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        currentPosition.x--;
        if (collision()) currentPosition.x++;
    } else if (event.key === 'ArrowRight') {
        currentPosition.x++;
        if (collision()) currentPosition.x--;
    } else if (event.key === 'ArrowDown') {
        moveTetromino();
    } else if (event.key === 'ArrowUp') {
        rotateTetromino();
    }
});

// Initialize the game
function initGame() {
    generateTetromino();
    drawBoard();
    gameLoop();
}

// LocalStorage functionality
document.addEventListener('DOMContentLoaded', () => {
    const highScore = localStorage.getItem('tetrisHighScore') || 0;
    alert(`High Score: ${highScore}`);
});

initGame();
