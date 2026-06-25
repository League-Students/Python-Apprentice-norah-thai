"""
# 20_Turtle_Tricks.py

In this assignment, you will use Tina the Turtle to draw a pentagon. 

- Each side of the pentagon should be a different color. 
- Use the turtle commands: tina.forward(), tina.left(), and tina.pencolor() to accomplish this.

Refer to the previous program, Meet_Tina.py, for examples of how to use turtle commands.
"""

# These lines are needed in most turtle programs
import turtle                           # Tell Python we want to work with the turtle
turtle.setup(600, 600, 0, 0)            # Set the size of the window
tina = turtle.Turtle()                  # Create a turtle named tina

# Use tina.forward() and tina.left() to draw a pentagon
# Make each side of the pentagon a different color with 
# tina.pencolor()

... # Your code here

turtle.exitonclick()                    # Close the window when we click on itimport turtle
import time

# --- 1. ENGINE CONFIGURATION & CANVAS ---
screen = turtle.Screen()
screen.title("Python Retro 2D Obby (Obstacle Course)")
screen.bgcolor("#0D1117")  # Cyber dark background
screen.setup(width=900, height=600)
screen.tracer(0)           # Manual frame rendering for smooth physics

# --- 2. GAME STATE VARIABLES ---
GRAVITY = -1.2
PLAYER_SPEED = 6
JUMP_STRENGTH = 18

# --- 3. PLATFORMS & HAZARDS SCHEMATICS ---
# Hardcoded coordinate arrays for the layout mapping
# Format: (X_Start, Y_Surface, Width, Height)
PLATFORMS_MAP = [
    (-450, -250, 250, 40),   # Spawn island base
    (-120, -180, 140, 20),   # Jump platform 1
    (80, -100, 120, 20),     # Jump platform 2
    (-100, -20, 100, 20),    # High reverse platform 3
    (-320, 60, 120, 20),     # Floating platform 4
    (-100, 150, 160, 20),    # Pre-finish ledge
    (240, 120, 220, 40)      # Victory checkpoint pad
]

# Lava Hazards mapping: stepping here resets the checkpoint
# Format: (X_Center, Y_Center, Width, Height)
HAZARDS_MAP = [
    (-200, -280, 200, 20),   # Floor pit pitfall 1
    (200, -280, 500, 20),    # Massive bottom lava pool
    (-10, -5, 20, 10),       # Spike block on platform 3
]

# --- 4. GRAPHICS ENTITIES CLASS CONSTRUCTORS ---
class BlockMesh(turtle.Turtle):
    """Draws rectangular blocks for platforms and hazards efficiently."""
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color(color)
        self.width_sz = width
        self.height_sz = height
        
        # Render the box shape manually via coordinates
        self.goto(x, y)
        self.begin_fill()
        for _ in range(2):
            self.forward(width)
            self.right(90)
            self.forward(height)
            self.right(90)
        self.end_fill()

# Render Obstacle Layers
for p in PLATFORMS_MAP:
    BlockMesh(p[0], p[1], p[2], p[3], "#30363D") # Slate Grey Platforms

for h in HAZARDS_MAP:
    # Compute corner offsets from center specs for the renderer loop
    hx = h[0] - (h[2] // 2)
    hy = h[1] + (h[3] // 2)
    BlockMesh(hx, hy, h[2], h[3], "#FF4500")    # Neon Orange Lava

# Win Flag Visual Indicator
flag = turtle.Turtle()
flag.shape("square")
flag.color("#00FF66") # Bright green goal node
flag.penup()
flag.goto(350, 150)

# Main Active Player Object
player = turtle.Turtle()
player.shape("square")
player.color("#58A6FF") # Neon Blue character
player.penup()

# Physics tracking values
player.velocity_y = 0
player.is_grounded = False

def respawn_player():
    """Returns player box to starting grid checkpoint."""
    player.goto(-350, -100)
    player.velocity_y = 0
    player.is_grounded = False

respawn_player()

# HUD text display system
hud = turtle.Turtle()
hud.color("#FFFFFF")
hud.penup()
hud.hideturtle()
hud.goto(0, 240)
hud.write("OBBY: Reach the Neon Green Platform!", align="center", font=("Courier", 16, "bold"))

# --- 5. PLAYER VECTOR KEYBOUNDS ---
moving_left = False
moving_right = False

def start_left(): global moving_left; moving_left = True
def stop_left():  global moving_left; moving_left = False
def start_right(): global moving_right; moving_right = True
def stop_right():  global moving_right; moving_right = False

def trigger_jump():
    """Gives structural vertical velocity push if sitting flat on surfaces."""
    if player.is_grounded:
        player.velocity_y = JUMP_STRENGTH
        player.is_grounded = False

# Complex Keyboard Bindings (tracks key down/up states for precision fluidity)
screen.listen()
screen.onkeypress(start_left, "Left")
screen.onkeyrelease(stop_left, "Left")
screen.onkeypress(start_right, "Right")
screen.onkeyrelease(stop_right, "Right")
screen.onkeypress(trigger_jump, "space")

# Alternative WASD
screen.onkeypress(start_left, "a")
screen.onkeyrelease(stop_left, "a")
screen.onkeypress(start_right, "d")
screen.onkeyrelease(stop_right, "d")
screen.onkeypress(trigger_jump, "w")

# --- 6. ENVIRONMENT RUNTIME PHYSICS ENGINE ---
game_active = True
while game_active:
    screen.update()
    time.sleep(0.015) # Constant framerate clock cycle throttling

    # A. Execute X Axis Horizontal Shifts
    if moving_left and player.xcor() > -440:
        player.setx(player.xcor() - PLAYER_SPEED)
    if moving_right and player.xcor() < 440:
        player.setx(player.xcor() + PLAYER_SPEED)

    # B. Gravity Acceleration Physics Applied Every Frame
    player.velocity_y += GRAVITY
    player.sety(player.ycor() + player.velocity_y)

    # Default to airborne unless collision logic flags otherwise
    player.is_grounded = False

    # Player dimension boxes for hitbox evaluations (Square is 20x20 pixels)
    p_left = player.xcor() - 10
    p_right = player.xcor() + 10
    p_bottom = player.ycor() - 10
    p_top = player.ycor() + 10

    # C. Axis Aligned Platform Solid Ground Collision Matrix
    for p in PLATFORMS_MAP:
        plat_left = p[0]
        plat_right = p[0] + p[2]
        plat_top = p[1]
        plat_bottom = p[1] - p[3]

        # Horizontal Overlap Verification
        if p_right > plat_left and p_left < plat_right:
            # Vertical Downward Falling Snapping Collision
            # Checks if player bottom passes through top ledge while moving down
            if player.velocity_y <= 0 and p_bottom <= plat_top and p_bottom >= plat_top + player.velocity_y - 2:
                player.sety(plat_top + 10) # Snap flush to surface line
                player.velocity_y = 0
                player.is_grounded = True
                break

    # D. Fatal Hazard Interaction Verification (Respawns on touch)
    for h in HAZARDS_MAP:
        h_left = h[0] - (h[2] // 2)
        h_right = h[0] + (h[2] // 2)
        h_top = h[1] + (h[3] // 2)
        h_bottom = h[1] - (h[3] // 2)

        if p_right > h_left and p_left < h_right and p_top > h_bottom and p_bottom < h_top:
            respawn_player()
            break

    # Absolute Bottom Killplane Fall-Zone Safe Check
    if player.ycor() < -290:
        respawn_player()

    # E. Victory Destination Validation Intersection
    if player.distance(flag) < 25:
        hud.goto(0, 0)
        hud.color("#00FF66")
        hud.write("OBBY COMPLETED! STAGE CLEAR", align="center", font=("Courier", 24, "bold"))
        game_active = False

