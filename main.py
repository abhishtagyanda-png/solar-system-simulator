import turtle

screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")

# Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(2)
sun.penup()

# Orbit path
orbit = turtle.Turtle()
orbit.hideturtle()
orbit.color("white")
orbit.penup()
orbit.goto(0, -150)
orbit.pendown()
orbit.circle(150)

# Earth
earth = turtle.Turtle()
earth.shape("circle")
earth.color("blue")
earth.penup()
earth.goto(150, 0)

screen.mainloop()