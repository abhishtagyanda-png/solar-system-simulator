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

def create_orbit(radius):
    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.color("white")
    orbit.penup()
    orbit.goto(0, -radius)
    orbit.pendown()
    orbit.circle(radius)

    create_orbit(80)
    create_orbit(120)
    create_orbit(150)
    create_orbit(220)

    
earth = Planet("Earth", "blue", 150, 0.005)

mercury = Planet("Mercury", "gray", 80, 0.01)

venus = Planet("Venus", "orange", 120, 0.007)

mars = Planet("Mars", "red", 220, 0.003)

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