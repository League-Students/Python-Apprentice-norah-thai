import turtle
import time

# 1. Screen Setup
win = turtle.Screen()
win.title("Ping Pong Game with Turtle")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Turns off automatic screen updates for smoother animation

# Score Tracking
score_a = 0
score_b = 0

# 2. Left Paddle (Paddle A)
paddle_a = turtle.Turtle()
paddle_a.speed(0)          # Animation speed (fastest)
paddle_a.shape("square")    # Standard shape
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)  # Stretches square into a vertical rectangle
paddle_a.penup()            # Prevents drawing lines when moving
paddle_a.goto(-350, 0)      # Initial position

# 3. Right Paddle (Paddle B)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# 4. The Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
# Ball speed variables (pixels moved per frame update)
ball.dx = 2.5
ball.dy = 2.5

# 5. Scoreboard Display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# 6. Paddle Movement Functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:  # Screen boundaries check
        paddle_a.sety(y + 20)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 20)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 20)

# 7. Keyboard Bindings
win.listen()
win.onkeypress(paddle_a_up, "w")      # Left player moves UP with 'W'
win.onkeypress(paddle_a_down, "s")    # Left player moves DOWN with 'S'
win.onkeypress(paddle_b_up, "Up")     # Right player moves UP with UP arrow
win.onkeypress(paddle_b_down, "Down") # Right player moves DOWN with DOWN arrow

# 8. Main Game Loop
while True:
    win.update()  # Manually update the screen frame
    time.sleep(0.01)  # Limits frame speed to prevent game from running too fast

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Top boundary collision
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1  # Reverse vertical direction

    # Bottom boundary collision
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Right goal (Player A scores)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1  # Send ball back toward the scoring player
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Left goal (Player B scores)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Paddle B Collision (Right)
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    # Paddle A Collision (Left)
    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1
