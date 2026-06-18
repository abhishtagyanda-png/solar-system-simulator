import turtle
import math
import time

# Create screen
screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")
screen.tracer(0)

# Create Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(2)
sun.penup()

# Draw orbit path
orbit = turtle.Turtle()
orbit.hideturtle()
orbit.color("white")
orbit.penup()
orbit.goto(0, -150)
orbit.pendown()
orbit.circle(150)

# Create Earth
earth = turtle.Turtle()
earth.shape("circle")
earth.color("blue")
earth.penup()

writer = turtle.Turtle()
writer.hideturtle()
writer.color("white")
writer.penup()
writer.goto(-250, 180)

# Orbit variables
angle = 0
radius = 150

# Animation loop
while True:
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    earth.goto(x, y)

    writer.clear()

    writer.write(
        f"Planet: Earth\nOrbit Radius: {radius}\nAngle: {angle:.2f}",
        font=("Arial", 14, "normal")
    )

    screen.update()

    angle += 0.005

    time.sleep(0.01)