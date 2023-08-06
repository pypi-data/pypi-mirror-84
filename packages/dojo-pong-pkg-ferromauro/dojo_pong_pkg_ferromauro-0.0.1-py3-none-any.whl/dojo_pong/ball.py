#! /usr/bin/env python3
import turtle

class Ball:
    def __init__(self,x,y):
        self.element = turtle.Turtle()
        self.element.speed(0)
        self.element.shape("circle")
        self.element.color("white")
        self.element.position = [x,y]
        self.__direction = [1,1]

    @property
    def position(self):
        return [self.element.xcor(),self.element.ycor()]

    @position.setter
    def position(self,x):
        self.element.penup()
        self.element.goto(x[0],x[1])

    @property
    def direction(self):
        return self.__direction
    
    @direction.setter
    def direction(self,d):
        self.__direction = [d[0], d[1]]
        
    def move(self):
        pos = self.position
        x = self.__direction[0]
        y = self.__direction[1]
        self.position = [pos[0] + 0.20*x, pos[1] + 0.20*y]

