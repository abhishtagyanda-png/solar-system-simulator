import turtle
import time
from planet import Planet


screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")
screen.tracer(0)


# Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(2)
sun.penup()


# Orbit function
def create_orbit(radius):
    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.color("white")
    orbit.penup()
    orbit.goto(0, -radius)
    orbit.pendown()
    orbit.circle(radius)


# Draw orbits
create_orbit(80)
create_orbit(120)
create_orbit(150)
create_orbit(220)


# Planets
earth = Planet("Earth", "blue", 150, 0.005)

mercury = Planet("Mercury", "gray", 80, 0.01)

venus = Planet("Venus", "orange", 120, 0.007)

mars = Planet("Mars", "red", 220, 0.003)


while True:

    earth.move()
    mercury.move()
    venus.move()
    mars.move()

    screen.update()

    time.sleep(0.01)