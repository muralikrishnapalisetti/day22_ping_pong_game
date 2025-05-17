import turtle
import time
import random

# Screen setup
screen = turtle.Screen()
screen.title("🔥 Fast PvP Pong Game 🔥")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Game duration and timer
GAME_DURATION = 120
start_time = time.time()

# Score variables
score_a = 0
score_b = 0

# Color list
colors = ["white", "cyan", "lime", "yellow", "red", "orange", "magenta"]

# Paddle A - Player 1
paddle_a = turtle.Turtle()
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B - Player 2
paddle_b = turtle.Turtle()
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.7  # Fast start
ball.dy = 0.7

# Score display
pen = turtle.Turtle()
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  |  Player B: 0", align="center", font=("Courier", 24, "bold"))

# Timer display
timer = turtle.Turtle()
timer.color("yellow")
timer.penup()
timer.hideturtle()
timer.goto(0, -270)


# Controls
def paddle_a_up():
    if paddle_a.ycor() < 250:
        paddle_a.sety(paddle_a.ycor() + 30)


def paddle_a_down():
    if paddle_a.ycor() > -240:
        paddle_a.sety(paddle_a.ycor() - 30)


def paddle_b_up():
    if paddle_b.ycor() < 250:
        paddle_b.sety(paddle_b.ycor() + 30)


def paddle_b_down():
    if paddle_b.ycor() > -240:
        paddle_b.sety(paddle_b.ycor() - 30)


# Key bindings
screen.listen()
screen.onkeypress(paddle_a_up, "w")
screen.onkeypress(paddle_a_down, "s")
screen.onkeypress(paddle_b_up, "Up")
screen.onkeypress(paddle_b_down, "Down")


# Update score
def update_score():
    pen.clear()
    pen.write(f"Player A: {score_a}  |  Player B: {score_b}", align="center", font=("Courier", 24, "bold"))


# Game loop
hit_count = 0
ball_speed_multiplier = 1.0


while True:
    screen.update()

    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Timer
    elapsed = time.time() - start_time
    time_left = max(0, int(GAME_DURATION - elapsed))
    timer.clear()
    timer.write(f"⏱ Time Left: {time_left}s", align="center", font=("Courier", 18, "bold"))

    if time_left <= 0:
        pen.goto(0, 0)
        winner = "Player A" if score_a > score_b else "Player B" if score_b > score_a else "Draw"
        pen.write(f"🏁 Game Over: {winner} Wins!", align="center", font=("Courier", 24, "bold"))
        break

    # Wall collisions
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.sety(ball.ycor())
        ball.dy *= -1

    # Paddle collisions
    if (340 < ball.xcor() < 350 and paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50) or \
            (-350 < ball.xcor() < -340 and paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.color(random.choice(colors))
        ball.dx *= -1
        ball.dy += random.choice([-0.2, 0.2])
        hit_count += 1
        if hit_count % 3 == 0:
            ball.dx *= 1.1
            ball.dy *= 1.1

    # Player B scores (A missed)
    if ball.xcor() < -390:
        score_b += 1
        ball_speed_multiplier *= 1.1  # Increase speed after score
        update_score()
        ball.goto(0, 0)
        ball.dx = 0.7 * ball_speed_multiplier
        ball.dy = random.choice([-0.7, 0.7]) * ball_speed_multiplier
        hit_count = 0

    # Player A scores (B missed)
    if ball.xcor() > 390:
        score_a += 1
        ball_speed_multiplier *= 1.1  # Increase speed after score
        update_score()
        ball.goto(0, 0)
        ball.dx = -0.7 * ball_speed_multiplier
        ball.dy = random.choice([-0.7, 0.7]) * ball_speed_multiplier
        hit_count = 0

    time.sleep(0.01)
