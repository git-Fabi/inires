// Pong Game Logic

const canvas = document.getElementById('pong');
const context = canvas.getContext('2d');

// Paddle dimensions
const paddleWidth = 10;
const paddleHeight = 100;

// Ball dimensions
const ballSize = 10;

// Score counters
let playerScore = 0;
let aiScore = 0;

// Initialize paddles and ball
const playerPaddle = {
    x: 0,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight
};

const aiPaddle = {
    x: canvas.width - paddleWidth,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: ballSize,
    speed: 4,
    velocityX: 4,
    velocityY: 4
};

// Score display
const scoreDisplay = document.createElement('div');
scoreDisplay.style.color = '#FFF';
scoreDisplay.style.fontSize = '24px';
document.body.appendChild(scoreDisplay);

// Game loop
function gameLoop() {
    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw paddles and ball
    context.fillStyle = '#000';
    context.fillRect(playerPaddle.x, playerPaddle.y, playerPaddle.width, playerPaddle.height);
    context.fillRect(aiPaddle.x, aiPaddle.y, aiPaddle.width, aiPaddle.height);
    context.beginPath();
    context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2, false);
    context.fill();
    
    // Update AI paddle position to follow the ball
    if (aiPaddle.y + paddleHeight / 2 < ball.y) {
        aiPaddle.y += 4;  // Move down
    } else if (aiPaddle.y + paddleHeight / 2 > ball.y) {
        aiPaddle.y -= 4;  // Move up
    }
    
    // Ball movement
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    
    // Collision detection
    if (ball.y - ball.radius < 0 || ball.y + ball.radius > canvas.height) {
        ball.velocityY = -ball.velocityY; // Reverse direction on top/bottom wall
    }
    if (ball.x - ball.radius < playerPaddle.x + playerPaddle.width && 
        ball.y > playerPaddle.y && 
        ball.y < playerPaddle.y + paddleHeight) {
        ball.velocityX = -ball.velocityX; // Reverse direction on player paddle
    }
    if (ball.x + ball.radius > aiPaddle.x && 
        ball.y > aiPaddle.y && 
        ball.y < aiPaddle.y + paddleHeight) {
        ball.velocityX = -ball.velocityX; // Reverse direction on AI paddle
    }
    
    // Scoring logic
    if (ball.x - ball.radius < 0) {
        aiScore++; // AI scores
        resetBall();
    } else if (ball.x + ball.radius > canvas.width) {
        playerScore++; // Player scores
        resetBall();
    }
    
    // Update score display
    scoreDisplay.innerHTML = `Player: ${playerScore} | AI: ${aiScore}`;

    requestAnimationFrame(gameLoop);
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.velocityX = (Math.random() > 0.5 ? 1 : -1) * ball.speed;
    ball.velocityY = (Math.random() > 0.5 ? 1 : -1) * ball.speed;
}

// Player input handling
document.addEventListener('keydown', function(event) {
    switch(event.key) {
        case 'ArrowUp':
            if (playerPaddle.y > 0) {
                playerPaddle.y -= 10;
            }
            break;
        case 'ArrowDown':
            if (playerPaddle.y < canvas.height - paddleHeight) {
                playerPaddle.y += 10;
            }
            break;
    }
});

// Start the game loop
gameLoop();
