import turtle
import math


class Planet:

    def __init__(self, name, color, orbit_radius, speed):

        self.name = name
        self.orbit_radius = orbit_radius
        self.angle = 0
        self.speed = speed

        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.color(color)
        self.body.penup()


    def move(self):

        x = self.orbit_radius * math.cos(self.angle)
        y = self.orbit_radius * math.sin(self.angle)

        self.body.goto(x, y)

        self.angle += self.speed