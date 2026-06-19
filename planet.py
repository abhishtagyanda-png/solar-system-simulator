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
        self.speed = speed
        self.angle = 0

        self.distance = distance
        self.period = period
        self.velocity = velocity

        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.color(color)
        self.body.shapesize(size)
        self.body.penup()

        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()

    def move(self):

        x = self.orbit_radius * math.cos(self.angle)
        y = self.orbit_radius * math.sin(self.angle)

        self.body.goto(x, y)

        self.label.clear()
        self.label.goto(x + 15, y + 15)
        self.label.write(
            self.name,
            font=("Arial", 8, "normal")
        )

        self.angle += self.speed