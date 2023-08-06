#! usr/bin/env python3
import turtle

class Paddle:
    def __init__(self,x,y):
        self.element = turtle.Turtle()
        self.element.speed(0)
        self.element.shape("square")
        self.element.color("white")
        self.element.shapesize(stretch_wid=5, stretch_len=1)
        self.position = [x, y]

    @property
    def position(self):
        return [self.element.xcor(),self.element.ycor()]

    @position.setter
    def position(self,x):
        self.element.penup()
        self.element.goto(x[0],x[1])

    def up(self):
        pos = self.position
        if pos[1] < 240:
            self.position = [pos[0], pos[1]+20]

    def down(self):
        pos = self.position
        if -240 < pos[1]: 
            self.position = [pos[0], pos[1]-20]
    
