import turtle
import time
import random
import math
from planet import Planet


# Screen Setup

screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")
screen.setup(width=1400, height=900)
screen.tracer(0)


# Sun

sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3.5)
sun.penup()

sun_label = turtle.Turtle()
sun_label.hideturtle()
sun_label.color("white")
sun_label.penup()
sun_label.goto(25, 25)
sun_label.write("Sun", font=("Arial", 10, "bold"))


# Orbit Drawing Function

def create_orbit(radius):

    orbit = turtle.Turtle()
    orbit.hideturtle()
    orbit.color("white")
    orbit.penup()

    orbit.goto(0, -radius)
    orbit.pendown()

    orbit.circle(radius)


# Orbits

create_orbit(50)
create_orbit(80)
create_orbit(110)
create_orbit(160)
create_orbit(230)
create_orbit(300)
create_orbit(370)
create_orbit(440)


asteroids = []

for _ in range(300):

    asteroid = turtle.Turtle()
    asteroid.shape("circle")
    asteroid.color("gray")
    asteroid.shapesize(0.15)
    asteroid.penup()

    radius = random.randint(180, 210)

    angle = random.uniform(
        0,
        2 * math.pi
    )

    speed = random.uniform(
        0.0005,
        0.0015
    )

    asteroid_data = {
        "body": asteroid,
        "radius": radius,
        "angle": angle,
        "speed": speed
    }

    asteroids.append(asteroid_data)

# Planets

mercury = Planet(
    "Mercury",
    "gray",
    50,
    0.01,
    "57.9 million km",
    "88 days",
    "47.36 km/s",
    0.4
)

venus = Planet(
    "Venus",
    "orange",
    80,
    0.007,
    "108.2 million km",
    "225 days",
    "35.02 km/s",
    0.8
)

earth = Planet(
    "Earth",
    "blue",
    110,
    0.005,
    "149.6 million km",
    "365 days",
    "29.78 km/s",
    0.8
)

mars = Planet(
    "Mars",
    "red",
    160,
    0.003,
    "227.9 million km",
    "687 days",
    "24.07 km/s",
    0.6
)

jupiter = Planet(
    "Jupiter",
    "orange",
    230,
    0.001,
    "778.5 million km",
    "11.86 years",
    "13.07 km/s",
    2.6
)

saturn = Planet(
    "Saturn",
    "gold",
    300,
    0.0008,
    "1.43 billion km",
    "29.46 years",
    "9.68 km/s",
     2.2
)

saturn_ring = turtle.Turtle()
saturn_ring.shape("circle")
saturn_ring.color("lightgray")
saturn_ring.penup()

# stretch the circle into an ellipse
saturn_ring.shapesize(stretch_wid=0.4, stretch_len=2.8)

saturn_ring.shapesize(
    stretch_wid=0.3,
    stretch_len=3.5
)

uranus = Planet(
    "Uranus",
    "cyan",
    370,
    0.0006,
    "2.87 billion km",
    "84 years",
    "6.80 km/s",
    1.3
)

neptune = Planet(
    "Neptune",
    "blue",
    440,
    0.0005,
    "4.50 billion km",
    "164.8 years",
    "5.43 km/s",
    1.3
)

def show_planet_info(planet):

    info_panel.clear()
    box.clear()

    # Draw box

    box.goto(-670, 330)
    box.pendown()

    for _ in range(2):
        box.forward(500)
        box.right(90)
        box.forward(400)
        box.right(90)

    box.penup()

    descriptions = {

        "Mercury":
        "Closest planet to the Sun.\nSmallest planet in the Solar System.",

        "Venus":
        "Second planet from the Sun.\nOften called Earth's twin.",

        "Earth":
        "Our home planet.\nOnly known planet with life.",

        "Mars":
        "The Red Planet.\nTarget of future human missions.",

        "Jupiter":
        "Largest planet in the Solar System.\nA giant gas world.",

        "Saturn":
        "Known for its spectacular ring system.",

        "Uranus":
        "An ice giant.\nRotates almost on its side.",

        "Neptune":
        "The most distant planet.\nKnown for powerful winds."
    }

    types = {

        "Mercury": "Terrestrial Planet",
        "Venus": "Terrestrial Planet",
        "Earth": "Terrestrial Planet",
        "Mars": "Terrestrial Planet",
        "Jupiter": "Gas Giant",
        "Saturn": "Gas Giant",
        "Uranus": "Ice Giant",
        "Neptune": "Ice Giant"
    }

    info_panel.goto(-650, 300)
    info_panel.write(
        f"""
{planet.name}

Type:
{types[planet.name]}

{descriptions[planet.name]}

Distance from Sun:
{planet.distance}

Orbital Period:
{planet.period}

Orbital Velocity:
{planet.velocity}
""",
        font=("Times New Roman", 12, "normal")
    )

# Main Loop

def handle_click(x, y):

    # Sun click

    if ((x - 0)**2 + (y - 0)**2) ** 0.5 < 35:

        info_panel.clear()
        box.clear()

        box.goto(-670, 330)
        box.pendown()

        for _ in range(2):
            box.forward(500)
            box.right(90)
            box.forward(400)
            box.right(90)

        box.penup()

        info_panel.goto(-30, 30)

        info_panel.write(
            """
Sun

Type:
G-Type Main Sequence Star

The Sun contains more than
99% of the Solar System's mass.

Age:
4.6 Billion Years

Surface Temperature:
5500 °C
""",
            font=("Times New Roman", 10, "normal")
        )

        return

    planets = [
        mercury,
        venus,
        earth,
        mars,
        jupiter,
        saturn,
        uranus,
        neptune
    ]

    for planet in planets:

        px = planet.body.xcor()
        py = planet.body.ycor()

        distance = ((x - px)**2 + (y - py)**2) ** 0.5

        if distance < 20:

            show_planet_info(planet)
            break

screen.onclick(handle_click)

info_panel = turtle.Turtle()
info_panel.hideturtle()
info_panel.color("white")
info_panel.penup()
info_panel.goto(-30, 30)

box = turtle.Turtle()
box.hideturtle()
box.color("white")
box.penup()

while True:

    mercury.move()
    venus.move()
    earth.move()
    mars.move()
    jupiter.move()
    saturn.move()

    saturn_ring.goto(
        saturn.body.xcor(),
        saturn.body.ycor()
    )

    uranus.move()
    neptune.move()

    for asteroid in asteroids:

        asteroid["angle"] += asteroid["speed"]

        x = (
            asteroid["radius"]
            * math.cos(asteroid["angle"])
        )

        y = (
            asteroid["radius"]
            * math.sin(asteroid["angle"])
        )

        asteroid["body"].goto(x, y)

    screen.update()
    time.sleep(0.01)