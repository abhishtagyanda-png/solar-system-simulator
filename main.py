import turtle
import time
from planet import Planet


# Screen setup
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


# Function to create orbit circles
def create_orbit(radius):

    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.color("white")
    orbit.penup()

    orbit.goto(0, -radius)
    orbit.pendown()

    orbit.circle(radius)


# Draw planet orbits
create_orbit(80)    # Mercury
create_orbit(120)   # Venus
create_orbit(150)   # Earth
create_orbit(220)   # Mars


# Create planets
mercury = Planet("Mercury", "gray", 80, 0.01)

venus = Planet("Venus", "orange", 120, 0.007)

earth = Planet("Earth", "blue", 150, 0.005)

mars = Planet("Mars", "red", 220, 0.003)


# Information text
info = turtle.Turtle()
info.hideturtle()
info.color("white")
info.penup()


# Animation loop
while True:

    # Move planets
    mercury.move()
    venus.move()
    earth.move()
    mars.move()


    # Update information
    info.clear()


    info.goto(-350, 200)
    info.write(
        f"Mercury\nOrbit Radius: {mercury.orbit_radius}",
        font=("Arial", 12, "normal")
    )


    info.goto(-350, 140)
    info.write(
        f"Venus\nOrbit Radius: {venus.orbit_radius}",
        font=("Arial", 12, "normal")
    )


    info.goto(-350, 80)
    info.write(
        f"Earth\nOrbit Radius: {earth.orbit_radius}",
        font=("Arial", 12, "normal")
    )


    info.goto(-350, 20)
    info.write(
        f"Mars\nOrbit Radius: {mars.orbit_radius}",
        font=("Arial", 12, "normal")
    )


    # Refresh screen
    screen.update()

    time.sleep(0.01)