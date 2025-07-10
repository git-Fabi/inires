// Unit tests for Tetris game logic
const assert = require('assert');

describe('Tetris Game', function() {
    describe('Tetromino Movement', function() {
        it('should start at the top center of the board', function() {
            // Test initialization of tetromino position
            generateTetromino();
            assert.strictEqual(currentPosition.x, 4); // 10/2 - 1
            assert.strictEqual(currentPosition.y, 0);
        });
    });

    describe('Collision Detection', function() {
        it('should detect collision with the board edges', function() {
            // Test collision with left edge
            currentPosition.x = -1;
            assert.strictEqual(collision(), true);

            // Test collision with right edge
            currentPosition.x = boardWidth;
            assert.strictEqual(collision(), true);
        });
    });

    describe('Clearing Lines', function() {
        it('should clear a completed line', function() {
            // Setup a completed line
            board[19] = Array(boardWidth).fill(1);
            clearLines();
            assert.strictEqual(board[19].every(cell => cell === 0), true);
        });
    });
});
