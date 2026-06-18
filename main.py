import turtle
import math
import time
from planet import Planet

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
earth = Planet("Earth", "blue", 150)

#Create Mercury
mercury = Planet("Mercury", "gray", 80)

# Create Venus
venus = Planet("Venus", "orange", 120)

# Create Mars
mars = Planet("Mars", "red", 200)

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

    earth.move()

    mercury.move()

    venus.move()

    mars.move()

    screen.update()

    time.sleep(0.01)