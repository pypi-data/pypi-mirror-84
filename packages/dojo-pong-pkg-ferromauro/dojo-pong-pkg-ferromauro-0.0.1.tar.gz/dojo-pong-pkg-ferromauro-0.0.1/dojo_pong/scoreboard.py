#! usr/bin/env python3
import turtle

class Scoreboard:
    def __init__(self):
        self.__score_a = 0
        self.__score_b = 0
        self.scoreboard = turtle.Turtle()
        self.scoreboard.speed(0)
        self.scoreboard.color("white")
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(0,260)
        self.scoreboard.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))
        

    @property
    def score_a(self):
        return self.__score_a
    
    @score_a.setter
    def score_a(self, a):
        self.__score_a = a

    @property
    def score_b(self):
        return self.__score_b
    
    @score_b.setter
    def score_b(self, b):
        self.__score_b = b

    def update(self,a,b):
        self.scoreboard.clear()
        self.scoreboard.write("Player A: {}  Player B: {}".format(a,b), align="center", font=("Courier", 24, "normal"))

