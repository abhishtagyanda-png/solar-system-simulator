"""
main.py
 
Animated, interactive Solar System Simulator — turtle edition.
 
Controls
--------
  Mouse hover      : show planet / Sun name tag + info in left panel
  Mouse click      : same as hover, but locks the panel until next click
  Scroll wheel     : zoom in / out  (Windows / Linux: Button-4/5)
  Z / X keys       : zoom in / out  (keyboard alternative)
  R key            : reset zoom to 1×
  Space / P key    : pause / resume
  Pause button     : bottom-left on-screen button
 
Run with:  python main.py
"""
 
import turtle
import random
import math
import tkinter as tk
 
 
# ---------------------------------------------------------------------------
# Screen — created first so we can query its real pixel size
# ---------------------------------------------------------------------------
 
screen = turtle.Screen()
screen.title("Solar System Simulator")
screen.bgcolor("black")
screen.setup(width=0.92, height=0.92)   # 92 % of the monitor
screen.tracer(0)
 
# Real pixel dimensions (after setup)
SW = screen.window_width()
SH = screen.window_height()
 
# Half-extents in turtle coords (origin = centre)
HW = SW // 2
HH = SH // 2
 
from planet import Planet   # noqa: E402  (needs screen to exist first)
 
 
# ---------------------------------------------------------------------------
# Layout geometry — computed from actual window size
# ---------------------------------------------------------------------------
 
# The simulation sits in the right-hand 75 % of the window.
# The left 25 % is reserved for the info panel + controls.
 
PANEL_MARGIN   = 5
PANEL_LEFT     = -HW + PANEL_MARGIN
PANEL_RIGHT    = -HW + int(SW * 0.23)   # ≈ 22 % of width
PANEL_TOP = HH - 60
PANEL_BOTTOM = -220        # leave room for button below
 
PANEL_WIDTH    = PANEL_RIGHT - PANEL_LEFT
PANEL_HEIGHT   = PANEL_TOP   - PANEL_BOTTOM
 
# Pause button sits at the very bottom-left
BTN_H          = 44
BTN_W          = PANEL_WIDTH
BUTTON_LEFT    = PANEL_LEFT
BUTTON_RIGHT   = PANEL_RIGHT
BUTTON_BOTTOM  = -HH + PANEL_MARGIN
BUTTON_TOP     = BUTTON_BOTTOM + BTN_H
 
# Zoom controls sit just above the pause button
ZOOM_H         = 44
ZOOM_BOTTOM    = BUTTON_TOP + PANEL_MARGIN
ZOOM_TOP       = ZOOM_BOTTOM + ZOOM_H
ZOOM_MID       = (ZOOM_BOTTOM + ZOOM_TOP) / 2
ZOOM_THIRD     = PANEL_WIDTH // 3

SPEED_H = 44

SPEED_BOTTOM = ZOOM_TOP + PANEL_MARGIN
SPEED_TOP = SPEED_BOTTOM + SPEED_H

SPEED_MID = (SPEED_BOTTOM + SPEED_TOP) / 2
 
# Simulation centre is shifted right so it doesn't overlap the panel
SIM_OFFSET_X = 130
# (keeps Sun roughly centred in the open space to the right of the panel)
 
# Base orbit radii — will be scaled up/down by zoom
BASE_ORBIT_RADII = [58, 90, 125, 180, 258, 330, 405, 475]
 
ASTEROID_COUNT        = 280
ASTEROID_RADIUS_RANGE = (210, 242)
ASTEROID_SPEED_RANGE  = (0.0005, 0.0015)
 
SUN_CLICK_RADIUS   = 38
PLANET_HOVER_RADIUS = 22
ANIMATION_DELAY_MS = 10
 
PLANET_TYPES = {
    "Mercury": "Terrestrial Planet",
    "Venus":   "Terrestrial Planet",
    "Earth":   "Terrestrial Planet",
    "Mars":   "Terrestrial Planet",
    "Jupiter": "Gas Giant",
    "Saturn":  "Gas Giant",
    "Uranus":  "Ice Giant",
    "Neptune": "Ice Giant",
}
 
PLANET_DESCRIPTIONS = {
    "Mercury": "Closest to the Sun.\nSmallest planet in the Solar System.",
    "Venus":   "Second from the Sun.\nCalled Earth's twin.",
    "Earth":   "Our home planet.\nOnly known world with life.",
    "Mars":    "The Red Planet.\nTarget of future human missions.",
    "Jupiter": "Largest planet in the Solar System.\nA colossal gas world.",
    "Saturn":  "Famous for its spectacular rings.\nA gas giant like Jupiter.",
    "Uranus":  "An ice giant.\nRotates almost on its side.",
    "Neptune": "The most distant planet.\nKnown for powerful storms.",
}
 
 
# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
 
state = {
    "paused": False,
    "zoom": 1.0,
    "zoom_min": 0.4,
    "zoom_max": 2.5,
    "zoom_step": 0.1,
    "speed_multiplier": 1.0,
    "hovered": None,
    "locked": None,
}
 
def increase_speed():

    state["speed_multiplier"] += 0.25

    if state["speed_multiplier"] > 5:
        state["speed_multiplier"] = 5

    if state["locked"] is None:
        show_intro_panel()

def decrease_speed():

    state["speed_multiplier"] -= 0.25

    if state["speed_multiplier"] < 0.25:
        state["speed_multiplier"] = 0.25

    if state["locked"] is None:
        show_intro_panel()

# ---------------------------------------------------------------------------
# Galaxy background
# ---------------------------------------------------------------------------
 
def draw_galaxy_background():
    bg = turtle.Turtle()
    bg.hideturtle()
    bg.penup()
    bg.speed(0)
 
    star_colors = ["white", "white", "lightblue", "lightyellow"]
    nebula_colors = ["purple", "darkviolet", "midnightblue", "indigo"]
 
    panel_edge = PANEL_RIGHT + 20   # keep nebula dots well clear of the panel
 
    # Faint nebula dust — only in corners / far right to avoid the sim area
    for _ in range(35):
        x = random.choice([
            random.randint(-HW + 10, panel_edge - 10),
            random.randint(int(HW * 0.6), HW - 10),
        ])
        y = random.choice([
            random.randint(int(HH * 0.55), HH - 10),
            random.randint(-HH + 10, -int(HH * 0.55)),
        ])
        bg.goto(x, y)
        bg.dot(random.randint(18, 45), random.choice(nebula_colors))
 
    # Stars scattered everywhere except inside the panel box
    for _ in range(260):
        while True:
            x = random.randint(-HW + 5, HW - 5)
            y = random.randint(-HH + 5, HH - 5)
            # Skip if inside the panel rectangle
            if not (PANEL_LEFT <= x <= PANEL_RIGHT and
                    PANEL_BOTTOM <= y <= PANEL_TOP):
                break
        bg.goto(x, y)
        bg.dot(random.randint(1, 3), random.choice(star_colors))
 
 
# ---------------------------------------------------------------------------
# Sun
# ---------------------------------------------------------------------------
 
sun_turtle = None
 
def draw_sun():
    global sun_turtle
    sun_turtle = turtle.Turtle()
    sun_turtle.shape("circle")
    sun_turtle.color("yellow")
    sun_turtle.shapesize(3.5)
    sun_turtle.penup()
    sun_turtle.goto(SIM_OFFSET_X, 0)
 
    lbl = turtle.Turtle()
    lbl.hideturtle()
    lbl.color("white")
    lbl.penup()
    lbl.goto(SIM_OFFSET_X + 28, 22)
    lbl.write("Sun", font=("Arial", 10, "bold"))
 
 
def sun_screen_pos():
    return SIM_OFFSET_X, 0
 
 
# ---------------------------------------------------------------------------
# Orbits
# ---------------------------------------------------------------------------
 
orbit_turtles = []
 
def draw_all_orbits():
    global orbit_turtles
    for t in orbit_turtles:
        t.clear()
        t.hideturtle()
    orbit_turtles = []
 
    for base_r in BASE_ORBIT_RADII:
        r = int(base_r * state["zoom"])
        ot = turtle.Turtle()
        ot.hideturtle()
        ot.color("gray40")
        ot.penup()
        ot.goto(SIM_OFFSET_X, -r)
        ot.pendown()
        ot.circle(r)
        ot.penup()
        orbit_turtles.append(ot)
 
 
# ---------------------------------------------------------------------------
# Asteroid belt
# ---------------------------------------------------------------------------
 
def create_asteroid_belt():
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.penup()
    drawer.speed(0)
 
    belt = [
        {
            "radius": random.randint(*ASTEROID_RADIUS_RANGE),
            "angle":  random.uniform(0, 2 * math.pi),
            "speed":  random.uniform(*ASTEROID_SPEED_RANGE),
        }
        for _ in range(ASTEROID_COUNT)
    ]
    return drawer, belt
 
 
def update_asteroid_belt(drawer, belt):
    drawer.clear()
    z = state["zoom"]
    for rock in belt:
        rock["angle"] += rock["speed"]
        r = rock["radius"] * z
        x = SIM_OFFSET_X + r * math.cos(rock["angle"])
        y =                 r * math.sin(rock["angle"])
        drawer.goto(x, y)
        drawer.dot(2, "gray55")
 
 
# ---------------------------------------------------------------------------
# Planets
# ---------------------------------------------------------------------------
 
def create_planets():
    return {
        "Mercury": Planet("Mercury", "gray",   58,  0.010, "57.9 million km",  "88 days",      "47.36 km/s", 0.40),
        "Venus":   Planet("Venus",   "orange", 90,  0.007, "108.2 million km", "225 days",     "35.02 km/s", 0.80),
        "Earth":   Planet("Earth",   "royalblue", 125, 0.005, "149.6 million km", "365 days",  "29.78 km/s", 0.80),
        "Mars":    Planet("Mars",    "red",    180, 0.003, "227.9 million km", "687 days",     "24.07 km/s", 0.60),
        "Jupiter": Planet("Jupiter", "orange", 258, 0.001, "778.5 million km", "11.86 years",  "13.07 km/s", 2.60),
        "Saturn":  Planet("Saturn",  "gold",   330, 0.0008,"1.43 billion km",  "29.46 years",  "9.68 km/s",  2.20),
        "Uranus":  Planet("Uranus",  "cyan",   405, 0.0006,"2.87 billion km",  "84 years",     "6.80 km/s",  1.30),
        "Neptune": Planet("Neptune", "blue",   475, 0.0005,"4.50 billion km",  "164.8 years",  "5.43 km/s",  1.30),
    }

planet_labels = {}
 
 
# ---------------------------------------------------------------------------
# Saturn's ring — compound annulus shape
# ---------------------------------------------------------------------------
 
def register_ring_shape(name, outer_rx, outer_ry, inner_rx, inner_ry,
                         ring_color, bg_color, steps=64):
    outer_pts = [
        (outer_rx * math.cos(t), outer_ry * math.sin(t))
        for t in (2 * math.pi * i / steps for i in range(steps))
    ]
    inner_pts = [
        (inner_rx * math.cos(t), inner_ry * math.sin(t))
        for t in (2 * math.pi * i / steps for i in range(steps))
    ]
    shape = turtle.Shape("compound")
    shape.addcomponent(outer_pts, ring_color, ring_color)
    shape.addcomponent(inner_pts, bg_color,   bg_color)
    screen.register_shape(name, shape)
 
 
def create_saturn_ring():
    register_ring_shape(
        "saturn_ring",
        outer_rx=42, outer_ry=16,
        inner_rx=25, inner_ry=10,
        ring_color="khaki",
        bg_color=screen.bgcolor(),
    )
    ring = turtle.Turtle()
    ring.shape("saturn_ring")
    ring.penup()
    return ring
 
 
# ---------------------------------------------------------------------------
# Info panel
# ---------------------------------------------------------------------------
 
box        = turtle.Turtle(); box.hideturtle();        box.penup();        box.speed(0)
info_panel = turtle.Turtle(); info_panel.hideturtle(); info_panel.penup(); info_panel.speed(0)
 
 
def draw_panel_box():
    box.clear()
    box.goto(PANEL_LEFT, PANEL_TOP)
    box.setheading(0)
    box.pendown()
    box.color("gray55", "gray10")
    box.begin_fill()
    for dist in [PANEL_WIDTH, PANEL_HEIGHT, PANEL_WIDTH, PANEL_HEIGHT]:
        box.forward(dist)
        box.right(90)
    box.end_fill()
    box.penup()
 
 
def write_panel(lines, heading_color="white"):
    """Write *lines* (a list of (text, font_tuple) pairs) top-down in the panel."""
    info_panel.clear()
    line_h = 18          # pixels per line (Verdana 11)
    x = PANEL_LEFT + 20
    y = PANEL_TOP - 40
    for text, font in lines:
        info_panel.color(heading_color if font[2] == "bold" else "white")
        info_panel.goto(x, y)
        info_panel.write(text, font=font)
        # count newlines in text to advance y correctly
        y -= line_h * (text.count("\n") + 1)
        heading_color = "white"   # only first line gets accent colour
 
 
def show_intro_panel():
    draw_panel_box()

    write_panel([
        ("☀ Solar System", ("Verdana", 12, "bold")),
        ("", ("Verdana", 4, "normal")),
        ("Hover a planet to see info.", ("Verdana", 10, "normal")),
        ("Click to lock the panel.", ("Verdana", 10, "normal")),
        ("Scroll or Z/X to zoom.", ("Verdana", 10, "normal")),
        ("", ("Verdana", 4, "normal")),
        (f"Simulation Speed: {state['speed_multiplier']}x",
         ("Verdana", 10, "normal")),
    ], heading_color="gold")
 
 
def show_planet_info(planet):
    draw_panel_box()
    desc = PLANET_DESCRIPTIONS[planet.name]
    write_panel([
        (planet.name,                          ("Verdana", 13, "bold")),
        (PLANET_TYPES[planet.name],            ("Verdana", 10, "italic")),
        ("",                                   ("Verdana", 3,  "normal")),
        (desc,                                 ("Verdana", 10, "normal")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Distance from Sun:",                 ("Verdana", 9,  "bold")),
        (planet.distance,                      ("Verdana", 10, "normal")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Orbital Period:",                    ("Verdana", 9,  "bold")),
        (planet.period,                        ("Verdana", 10, "normal")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Orbital Velocity:",                  ("Verdana", 9,  "bold")),
        (planet.velocity,                      ("Verdana", 10, "normal")),
    ], heading_color="cyan")
 
 
def show_sun_info():
    draw_panel_box()
    write_panel([
        ("Sun",                                ("Verdana", 13, "bold")),
        ("G-Type Main-Sequence Star",          ("Verdana", 10, "italic")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Contains >99 % of the Solar",        ("Verdana", 10, "normal")),
        ("System's total mass.",               ("Verdana", 10, "normal")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Age:",                               ("Verdana", 9,  "bold")),
        ("4.6 Billion Years",                  ("Verdana", 10, "normal")),
        ("",                                   ("Verdana", 3,  "normal")),
        ("Surface Temperature:",               ("Verdana", 9,  "bold")),
        ("5,500 °C",                           ("Verdana", 10, "normal")),
    ], heading_color="yellow")
 
 
# ---------------------------------------------------------------------------
# Pause / Resume button
# ---------------------------------------------------------------------------
 
btn_box   = turtle.Turtle(); btn_box.hideturtle();   btn_box.penup();   btn_box.speed(0)
btn_label = turtle.Turtle(); btn_label.hideturtle(); btn_label.penup(); btn_label.speed(0)
 
 
def draw_pause_button():
    btn_box.clear()
    btn_box.goto(BUTTON_LEFT, BUTTON_TOP)
    btn_box.setheading(0)
    btn_box.pendown()
    color = "steelblue" if state["paused"] else "gray30"
    btn_box.color("white", color)
    btn_box.begin_fill()
    for dist in [BTN_W, BTN_H, BTN_W, BTN_H]:
        btn_box.forward(dist)
        btn_box.right(90)
    btn_box.end_fill()
    btn_box.penup()
 
    btn_label.clear()
    btn_label.color("white")
    text = "▶  Resume" if state["paused"] else "⏸  Pause"
    mid_x = BUTTON_LEFT + BTN_W / 2
    mid_y = BUTTON_BOTTOM + BTN_H / 2 - 7
    btn_label.goto(mid_x, mid_y)
    btn_label.write(text, align="center", font=("Arial", 12, "bold"))
 
 
def toggle_pause():
    state["paused"] = not state["paused"]
    draw_pause_button()
 
 
# ---------------------------------------------------------------------------
# Zoom controls (three buttons: –  zoom%  +)
# ---------------------------------------------------------------------------
 
zoom_box   = turtle.Turtle(); zoom_box.hideturtle();   zoom_box.penup();   zoom_box.speed(0)
zoom_label = turtle.Turtle(); zoom_label.hideturtle(); zoom_label.penup(); zoom_label.speed(0)

speed_box = turtle.Turtle()
speed_box.hideturtle()
speed_box.penup()

speed_label = turtle.Turtle()
speed_label.hideturtle()
speed_label.penup()

def draw_speed_controls():

    speed_box.clear()
    speed_label.clear()

    bw = PANEL_WIDTH

    speed_box.goto(PANEL_LEFT, SPEED_TOP)
    speed_box.setheading(0)

    speed_box.pendown()
    speed_box.color("gray55", "gray15")

    speed_box.begin_fill()

    for dist in [bw, SPEED_H, bw, SPEED_H]:
        speed_box.forward(dist)
        speed_box.right(90)

    speed_box.end_fill()
    speed_box.penup()

    for frac in [1/3, 2/3]:
        speed_box.goto(PANEL_LEFT + int(bw * frac), SPEED_TOP)
        speed_box.pendown()
        speed_box.goto(PANEL_LEFT + int(bw * frac), SPEED_BOTTOM)
        speed_box.penup()

    third = bw // 3

    cx_minus = PANEL_LEFT + third // 2
    cx_speed = PANEL_LEFT + third + third // 2
    cx_plus = PANEL_LEFT + 2 * third + third // 2

    ty = SPEED_MID - 8

    speed_label.color("white")

    speed_label.goto(cx_minus, ty)
    speed_label.write("-", align="center",
                      font=("Arial", 16, "bold"))

    speed_label.goto(cx_speed, ty)
    speed_label.write(
        f"{state['speed_multiplier']:.2f}x",
        align="center",
        font=("Arial", 10, "bold")
    )

    speed_label.goto(cx_plus, ty)
    speed_label.write("+", align="center",
                      font=("Arial", 16, "bold"))
 
 
def draw_zoom_controls():
    zoom_box.clear()
    zoom_label.clear()
 
    bw = PANEL_WIDTH
    # Outer box
    zoom_box.goto(PANEL_LEFT, ZOOM_TOP)
    zoom_box.setheading(0)
    zoom_box.pendown()
    zoom_box.color("gray55", "gray15")
    zoom_box.begin_fill()
    for dist in [bw, ZOOM_H, bw, ZOOM_H]:
        zoom_box.forward(dist)
        zoom_box.right(90)
    zoom_box.end_fill()
    zoom_box.penup()
 
    # Dividers between – | label | +
    for frac in [1/3, 2/3]:
        zoom_box.goto(PANEL_LEFT + int(bw * frac), ZOOM_TOP)
        zoom_box.pendown()
        zoom_box.goto(PANEL_LEFT + int(bw * frac), ZOOM_BOTTOM)
        zoom_box.penup()
 
    # Labels
    zoom_label.color("white")
    third = bw // 3
    cx_minus  = PANEL_LEFT + third // 2
    cx_pct    = PANEL_LEFT + third + third // 2
    cx_plus   = PANEL_LEFT + 2 * third + third // 2
    ty = ZOOM_MID - 8
 
    zoom_label.goto(cx_minus, ty)
    zoom_label.write("−", align="center", font=("Arial", 16, "bold"))
 
    pct = int(state["zoom"] * 100)
    zoom_label.goto(cx_pct, ty)
    zoom_label.write(f"{pct} %", align="center", font=("Arial", 11, "bold"))
 
    zoom_label.goto(cx_plus, ty)
    zoom_label.write("+", align="center", font=("Arial", 16, "bold"))
 
 
def apply_zoom(new_zoom):
    new_zoom = max(state["zoom_min"], min(state["zoom_max"], new_zoom))
    state["zoom"] = round(new_zoom, 2)
    for p in planets.values():
        p.set_zoom(state["zoom"])
    draw_all_orbits()
    draw_zoom_controls()
 
 
def zoom_in():
    apply_zoom(state["zoom"] + state["zoom_step"])
 
 
def zoom_out():
    apply_zoom(state["zoom"] - state["zoom_step"])
 
 
def zoom_reset():
    apply_zoom(1.0)
 
 
# ---------------------------------------------------------------------------
# Click / hover geometry helpers
# ---------------------------------------------------------------------------
 
def point_in_box(x, y, left, right, bottom, top):
    return left <= x <= right and bottom <= y <= top
 
 
def hit_planet(mx, my):
    """Return the Planet under (mx,my), or None."""
    for p in planets.values():
        px, py = p.position()
        if math.hypot(mx - px, my - py) < PLANET_HOVER_RADIUS:
            return p
    return None
 
 
def hit_sun(mx, my):
    sx, sy = sun_screen_pos()
    return math.hypot(mx - sx, my - sy) < SUN_CLICK_RADIUS
 
 
# ---------------------------------------------------------------------------
# Click handler
# ---------------------------------------------------------------------------
 
def handle_click(mx, my):
    # Pause button
    if point_in_box(mx, my, BUTTON_LEFT, BUTTON_RIGHT, BUTTON_BOTTOM, BUTTON_TOP):
        toggle_pause()
        return
 
    # Zoom minus
    if point_in_box(mx, my, PANEL_LEFT, PANEL_LEFT + PANEL_WIDTH // 3,
                    ZOOM_BOTTOM, ZOOM_TOP):
        zoom_out()
        return
 
    # Zoom plus
    if point_in_box(mx, my, PANEL_LEFT + 2 * PANEL_WIDTH // 3, PANEL_RIGHT,
                    ZOOM_BOTTOM, ZOOM_TOP):
        zoom_in()
        return
 
    # Sun
    if hit_sun(mx, my):
        state["locked"] = "Sun"
        show_sun_info()
        return
 
    # Planet
    p = hit_planet(mx, my)
    if p:
        state["locked"] = p.name
        show_planet_info(p)
        return
 
    # Click on empty space → unlock panel
    state["locked"] = None
    show_intro_panel()
 
 
# ---------------------------------------------------------------------------
# Hover handler (motion event via Tkinter canvas)
# ---------------------------------------------------------------------------
 
def handle_motion(event):
    """Called by Tkinter on every mouse-move over the canvas."""
    # Convert Tkinter canvas coords → turtle world coords
    canvas = screen.getcanvas()
    mx = canvas.canvasx(event.x) - SW / 2
    my = SH / 2 - canvas.canvasy(event.y)
 
    # Don't override a locked panel
    if state["locked"] is not None:
        return
 
    p = hit_planet(mx, my)
    if p:
        if state["hovered"] != p.name:
            state["hovered"] = p.name
            show_planet_info(p)
    elif hit_sun(mx, my):
        if state["hovered"] != "Sun":
            state["hovered"] = "Sun"
            show_sun_info()
    else:
        if state["hovered"] is not None:
            state["hovered"] = None
            show_intro_panel()
 
 
# ---------------------------------------------------------------------------
# Keyboard bindings
# ---------------------------------------------------------------------------
 
def bind_keys():
    screen.listen()
    screen.onkey(toggle_pause, "space")
    screen.onkey(toggle_pause, "p")
    screen.onkey(zoom_in,      "z")
    screen.onkey(zoom_out,     "x")
    screen.onkey(zoom_reset,   "r")

    screen.onkey(increase_speed, "Up")
    screen.onkey(decrease_speed, "Down")
 
 
# ---------------------------------------------------------------------------
# Animation loop
# ---------------------------------------------------------------------------
 
def animate():
    if not state["paused"]:
        for name, p in planets.items():
            # Offset planet position by SIM_OFFSET_X so Sun stays centred
            # in the open right-hand area
            p.body.goto(
                SIM_OFFSET_X + p.orbit_radius * math.cos(p.angle),
                              p.orbit_radius * math.sin(p.angle),
            )
            p.angle += (
    p.speed *
    state["speed_multiplier"] )

            planet_labels[name].clear()

            planet_labels[name].goto(
                p.body.xcor() + 12,
                p.body.ycor() + 12
            )

            planet_labels[name].write(
                name,
                font=("Arial", 8, "normal")
            )
 
        saturn = planets["Saturn"]
        saturn_ring.goto(saturn.body.xcor(), saturn.body.ycor())
 
        update_asteroid_belt(asteroid_drawer, asteroids)
 
    screen.update()
    screen.ontimer(animate, ANIMATION_DELAY_MS)
 
 
# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
    draw_galaxy_background()
    draw_sun()
    draw_all_orbits()
 
    asteroid_drawer, asteroids = create_asteroid_belt()
    planets = create_planets()

    for name in planets:
        label = turtle.Turtle()
        label.hideturtle()
        label.penup()
        label.color("white")
        planet_labels[name] = label

    saturn_ring = create_saturn_ring()
 
    # Apply initial zoom so planets carry the SIM_OFFSET_X correctly
    for p in planets.values():
        p.set_zoom(state["zoom"])
 
    show_intro_panel()
    draw_pause_button()
    draw_zoom_controls()
 
    screen.onclick(handle_click)
 
    # Hook mouse-motion into the underlying Tkinter canvas
    canvas = screen.getcanvas()
    canvas.bind("<Motion>", handle_motion)
 
    bind_keys()
 
    animate()
    screen.mainloop()