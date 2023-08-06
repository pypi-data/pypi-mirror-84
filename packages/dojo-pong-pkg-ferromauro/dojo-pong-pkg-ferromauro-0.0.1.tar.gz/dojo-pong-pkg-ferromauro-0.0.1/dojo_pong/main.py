#! usr/bin/env python3

import turtle
import winsound
import random

from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

# Setup window
wn = turtle.Screen()
wn.title("Dojo-Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Object generation
paddle_a = Paddle(-365,0)
paddle_b = Paddle(365,0)
ball_1 = Ball(0,0)
ball_1.direction = [1,1]
scoreboard = Scoreboard()

# Key bindings
wn.listen()
wn.onkeypress(paddle_a.up, "w")
wn.onkeypress(paddle_a.down, "s")
wn.onkeypress(paddle_b.up, "Up")
wn.onkeypress(paddle_b.down, "Down")

# Main game loop
while True:
    wn.update()

    ball_1.move()
  
#border check
    if ball_1.position[1] > 290:        
        x_temp = ball_1.direction[0] 
        ball_1.direction = [x_temp,-1]
        winsound.Beep(1000, 100)

    if ball_1.position[1] < -290:
        x_temp = ball_1.direction[0] 
        ball_1.direction = [x_temp,1]
        winsound.Beep(1000, 100)
    
    if ball_1.position[0] > 390:
        ball_1.position = [0,0]
        ball_1.direction =[-1,-1]
        score_a = scoreboard.score_a
        scoreboard.score_a = score_a + 1
        scoreboard.update(scoreboard.score_a, scoreboard.score_b)
        winsound.Beep(200, 1000)

    if ball_1.position[0] < -390:
        ball_1.position = [0,0]
        ball_1.direction = [1,1]
        score_b = scoreboard.score_b
        scoreboard.score_b = score_b + 1
        scoreboard.update(scoreboard.score_a, scoreboard.score_b)
        winsound.Beep(200, 1000)

# Check collision
    if (ball_1.position[0] > 340 and ball_1.position[0] < 350) and ball_1.position[1] < paddle_b.position[1] + 50 and ball_1.position[1] > paddle_b.position[1] -50:
        y_temp = ball_1.direction[1] 
        ball_1.direction = [-1, y_temp*random.randint(1,5)/4]
        winsound.Beep(1200, 50)

    if (ball_1.position[0] <  -340 and ball_1.position[0] > -350) and ball_1.position[1] < paddle_a.position[1] + 50 and ball_1.position[1] > paddle_a.position[1] -50:
        y_temp = ball_1.direction[1]
        ball_1.direction = [1, -y_temp*random.randint(1,5)/4]
        winsound.Beep(1000, 50)
