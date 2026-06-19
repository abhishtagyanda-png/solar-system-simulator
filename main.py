import turtle
import time
from planet import Planet


# Screen setup
screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")
screen.setup(width=1400, height=900)
screen.tracer(0)


# Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(4)
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


# Draw orbits

create_orbit(80)      # Mercury
create_orbit(120)     # Venus
create_orbit(150)     # Earth
create_orbit(220)     # Mars
create_orbit(320)     # Jupiter
create_orbit(420)     # Saturn
create_orbit(520)     # Uranus
create_orbit(620)     # Neptune


# Create planets

mercury = Planet(
    "Mercury",
    "gray",
    80,
    0.01,
    "57.9 million km",
    "88 days",
    "47.36 km/s",
    0.4
)

venus = Planet(
    "Venus",
    "orange",
    120,
    0.007,
    "108.2 million km",
    "225 days",
    "35.02 km/s",
    0.8
)

earth = Planet(
    "Earth",
    "blue",
    150,
    0.005,
    "149.6 million km",
    "365 days",
    "29.78 km/s",
    0.8
)

mars = Planet(
    "Mars",
    "red",
    220,
    0.003,
    "227.9 million km",
    "687 days",
    "24.07 km/s",
    0.6
)

jupiter = Planet(
    "Jupiter",
    "orange",
    320,
    0.001,
    "778.5 million km",
    "11.86 years",
    "13.07 km/s",
    2.0
)

saturn = Planet(
    "Saturn",
    "gold",
    420,
    0.0008,
    "1.43 billion km",
    "29.46 years",
    "9.68 km/s",
    1.8
)

uranus = Planet(
    "Uranus",
    "light blue",
    520,
    0.0006,
    "2.87 billion km",
    "84 years",
    "6.80 km/s",
    1.3
)

neptune = Planet(
    "Neptune",
    "dark blue",
    620,
    0.0005,
    "4.50 billion km",
    "164.8 years",
    "5.43 km/s",
    1.3
)


# Information panel

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
    jupiter.move()
    saturn.move()
    uranus.move()
    neptune.move()

    # Update information

    info.clear()

    info.goto(-650, 300)

    info.write(
        """
PLANETS

Mercury
Venus
Earth
Mars
Jupiter
Saturn
Uranus
Neptune

Version 4 In Progress
        """,
        font=("Arial", 12, "normal")
    )

    screen.update()

    time.sleep(0.01)