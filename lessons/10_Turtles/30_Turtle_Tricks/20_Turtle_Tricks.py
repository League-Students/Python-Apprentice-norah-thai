win = turtle.Screen()
win.title("Ping Pong Game with Turtle")
win.bgcolor("black")

# Dynamically calculate the center coordinates of your specific monitor
window_width = 800
window_height = 600
screen_width = win.window_width()
screen_height = win.window_height()

# Set positions based on your display's resolution
center_x = int((screen_width / 2) - (window_width / 2))
center_y = int((screen_height / 2) - (window_height / 2))

# Force the window to spawn precisely in the middle
win.setup(width=window_width, height=window_height, startx=center_x, starty=center_y)
win.tracer(0)  
