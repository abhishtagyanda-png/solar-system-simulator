import turtle
import math


class Planet:

    def __init__(
        self,
        name,
        color,
        orbit_radius,
        speed,
        distance,
        period,
        velocity,
        size
    ):

        self.name = name
        self.orbit_radius = orbit_radius
        self.angle = 0
        self.speed = speed

        self.distance = distance
        self.period = period
        self.velocity = velocity
        self.size = size

        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.shapesize(size)
        self.body.color(color)
        self.body.penup()


    def move(self):

        x = self.orbit_radius * math.cos(self.angle)
        y = self.orbit_radius * math.sin(self.angle)

        self.body.goto(x, y)

        self.angle += self.speed