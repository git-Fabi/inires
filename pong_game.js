// Pong Game Logic
const gameArea = document.getElementById('gameArea');
const playerPaddle = document.getElementById('playerPaddle');
const aiPaddle = document.getElementById('aiPaddle');
const ball = document.getElementById('ball');
const playerScoreDisplay = document.getElementById('playerScore');
const aiScoreDisplay = document.getElementById('aiScore');

let ballSpeedX = 5;
let ballSpeedY = 5;
let playerScore = 0;
let aiScore = 0;
let ballPosition = { x: gameArea.clientWidth / 2, y: gameArea.clientHeight / 2 };

function resetBall() {
    ballPosition = { x: gameArea.clientWidth / 2, y: gameArea.clientHeight / 2 };
    ball.style.left = `${ballPosition.x}px`;
    ball.style.top = `${ballPosition.y}px`;
}

function movePaddles(event) {
    const paddleHeight = playerPaddle.clientHeight;
    if (event.key === 'ArrowUp' && playerPaddle.offsetTop > 0) {
        playerPaddle.style.top = `${playerPaddle.offsetTop - 20}px`;
    } else if (event.key === 'ArrowDown' && (playerPaddle.offsetTop + paddleHeight) < gameArea.clientHeight) {
        playerPaddle.style.top = `${playerPaddle.offsetTop + 20}px`;
    }
}

function updateGame() {
    // Update ball position
    ballPosition.x += ballSpeedX;
    ballPosition.y += ballSpeedY;

    // Collision detection
    if (ballPosition.y <= 0 || ballPosition.y >= gameArea.clientHeight - ball.clientHeight) {
        ballSpeedY = -ballSpeedY;
    }

    if (ballPosition.x <= playerPaddle.offsetWidth && ballPosition.y >= playerPaddle.offsetTop && ballPosition.y <= playerPaddle.offsetTop + playerPaddle.clientHeight) {
        ballSpeedX = -ballSpeedX;
    } else if (ballPosition.x >= gameArea.clientWidth - aiPaddle.offsetWidth - ball.clientWidth && ballPosition.y >= aiPaddle.offsetTop && ballPosition.y <= aiPaddle.offsetTop + aiPaddle.clientHeight) {
        ballSpeedX = -ballSpeedX;
    }

    // Scoring
    if (ballPosition.x <= 0) {
        aiScore++;
        aiScoreDisplay.innerText = aiScore;
        resetBall();
    } else if (ballPosition.x >= gameArea.clientWidth - ball.clientWidth) {
        playerScore++;
        playerScoreDisplay.innerText = playerScore;
        resetBall();
    }

    ball.style.left = `${ballPosition.x}px`;
    ball.style.top = `${ballPosition.y}px`;
}

function aiMovement() {
    const aiPaddleCenter = aiPaddle.offsetTop + (aiPaddle.clientHeight / 2);
    if (ballPosition.y < aiPaddleCenter && aiPaddle.offsetTop > 0) {
        aiPaddle.style.top = `${aiPaddle.offsetTop - 5}px`;
    } else if (ballPosition.y > aiPaddleCenter && (aiPaddle.offsetTop + aiPaddle.clientHeight) < gameArea.clientHeight) {
        aiPaddle.style.top = `${aiPaddle.offsetTop + 5}px`;
    }
}

setInterval(() => {
    updateGame();
    aiMovement();
}, 1000 / 60);

document.addEventListener('keydown', movePaddles);
resetBall();
