
"""
planet.py
 
Defines the Planet class used by the Solar System Simulator.
 
Each Planet owns two turtles:
  - body  : the visible dot that orbits the Sun.
  - label : a separate turtle for the floating name tag shown on hover.
 
Zoom is applied externally by main.py via planet.set_zoom(factor).
"""
 
import turtle
import math
 
 
class Planet:
    """A single orbiting body in the simulation."""
 
    def __init__(self, name, color, orbit_radius, speed,
                 distance, period, velocity, size):
        self.name = name
        self.base_orbit_radius = orbit_radius   # original, never mutated
        self.orbit_radius = orbit_radius        # scaled by zoom
        self.speed = speed
        self.angle = 0.0
        self.base_size = size                   # shapesize at zoom 1.0
        self._zoom = 1.0
 
        # Informational text shown in the side panel when clicked / hovered
        self.distance = distance
        self.period = period
        self.velocity = velocity
 
        # Visible planet body
        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.color(color)
        self.body.shapesize(size)
        self.body.pencolor(color)
        self.body.pensize(1)

        self.trails_enabled = True
 
        # Floating name label (shown on hover)
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()
 
    # ------------------------------------------------------------------
    # Zoom
    # ------------------------------------------------------------------
 
    def set_zoom(self, factor):
        """Rescale orbit radius and body size to match zoom factor."""
        self._zoom = factor
        self.orbit_radius = self.base_orbit_radius * factor
        clamped_size = max(0.2, self.base_size * factor)
        self.body.shapesize(clamped_size)
 
    # ------------------------------------------------------------------
    # Motion
    # ------------------------------------------------------------------
 
    def move(self):
        """Advance the planet one animation step along its orbit."""
        x = self.orbit_radius * math.cos(self.angle)
        y = self.orbit_radius * math.sin(self.angle)
        self.body.goto(x, y)
        self.angle += self.speed
 
    # ------------------------------------------------------------------
    # Label (hover tooltip — shown / hidden by main.py)
    # ------------------------------------------------------------------
 
    def show_label(self):
        x, y = self.position()
        self.label.clear()
        self.label.goto(x + 15, y + 15)
        self.label.write(self.name, font=("Arial", 9, "bold"))
 
    def hide_label(self):
        self.label.clear()
 
    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
 
    def position(self):
        """(x, y) screen position — used for click / hover detection."""
        return self.body.xcor(), self.body.ycor()
