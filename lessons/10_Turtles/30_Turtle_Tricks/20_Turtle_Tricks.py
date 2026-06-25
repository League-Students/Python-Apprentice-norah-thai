import turtle
import time

# 1. SETUP GAME SCREEN
screen = turtle.Screen()
screen.title("Simple Ping-Pong")
screen.bgcolor("black")
screen.setup(width=600, height=400)
screen.tracer(0)

# 2. CREATE PADDLE
paddle = turtle.Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=1, stretch_len=5) # Make it wide
paddle.color("cyan")
paddle.penup()
paddle.goto(0, -160)

# 3. CREATE BALL
ball = turtle.Turtle()
ball.shape("circle")
ball.color("pink")
ball.penup()
ball.goto(0, 0)

# Ball speed directions
ball_x_speed = 3
ball_y_speed = 3

# 4. CONTROLS
def move_left():
    if paddle.xcor() > -240:
        paddle.setx(paddle.xcor() - 30)

def move_right():
    if paddle.xcor() < 240:
        paddle.setx(paddle.xcor() + 30)

# Link keyboard keys
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# 5. MAIN GAME LOOP
while True:
    screen.update()
    time.sleep(0.01) # Keeps game at regular speed

    # Move the ball
    ball.setx(ball.xcor() + ball_x_speed)
    ball.sety(ball.ycor() + ball_y_speed)

    # Bounce off Left or Right walls
    if ball.xcor() > 280 or ball.xcor() < -280:
        ball_x_speed = ball_x_speed * -1

    # Bounce off Ceiling
    if ball.ycor() > 180:
        ball_y_speed = ball_y_speed * -1

    # Bounce off the Paddle
    if ball.ycor() < -140 and paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50:
        ball_y_speed = ball_y_speed * -1

    # Miss the ball (Reset to middle)
    if ball.ycor() < -200:
        ball.goto(0, 0)
        ball_y_speed = 3 # Send it back up
