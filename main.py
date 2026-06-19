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



# Draw orbits

create_orbit(80)     # Mercury
create_orbit(120)    # Venus
create_orbit(150)    # Earth
create_orbit(220)    # Mars
create_orbit(300)    # Jupiter



# Create planets

mercury = Planet(
    "Mercury",
    "gray",
    80,
    0.01,
    "57.9 million km",
    "88 days",
    "47.36 km/s"
)


venus = Planet(
    "Venus",
    "orange",
    120,
    0.007,
    "108.2 million km",
    "225 days",
    "35.02 km/s"
)


earth = Planet(
    "Earth",
    "blue",
    150,
    0.005,
    "149.6 million km",
    "365 days",
    "29.78 km/s"
)


mars = Planet(
    "Mars",
    "red",
    220,
    0.003,
    "227.9 million km",
    "687 days",
    "24.07 km/s"
)

jupiter = Planet(
    "Jupiter",  
    "orange",
    300,        
    0.001,
    "778.5 million km",
    "4333 days",
    "13.07 km/s"
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

    # Clear text

    info.clear()



    # Mercury

    info.goto(-450, 250)

    info.write(
        f"""Mercury

Distance:
{mercury.distance}

Period:
{mercury.period}

Velocity:
{mercury.velocity}""",
        font=("Arial", 10, "normal")
    )



    # Venus

    info.goto(-450, 80)

    info.write(
        f"""Venus

Distance:
{venus.distance}

Period:
{venus.period}

Velocity:
{venus.velocity}""",
        font=("Arial", 10, "normal")
    )



    # Earth

    info.goto(-450, -90)

    info.write(
        f"""Earth

Distance:
{earth.distance}

Period:
{earth.period}

Velocity:
{earth.velocity}""",
        font=("Arial", 10, "normal")
    )



    # Mars

    info.goto(-450, -260)

    info.write(
        f"""Mars

Distance:
{mars.distance}

Period:
{mars.period}

Velocity:
{mars.velocity}""",
        font=("Arial", 10, "normal")
    )

    # Jupiter

    info.goto(-450, -430)

    info.write(
        f"""Jupiter

Distance:
{jupiter.distance}

Period:
{jupiter.period}

Velocity:
{jupiter.velocity}""",
        font=("Arial", 10, "normal")
    )

    screen.update()

    time.sleep(0.01)