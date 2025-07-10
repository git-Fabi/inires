
// Function to reset the game state
function resetGame() {
    board.forEach(row => row.fill(0)); // Clear the board
    score = 0; // Reset score
    gameOver = false; // Reset game over status
    // Additional reset logic if needed
}

// Update initGame function to include resetGame
function initGame() {
    resetGame();
    generateTetromino();
    gameLoop();
}