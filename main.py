import tkinter as tk
import display

# System setup variables
root: tk.Tk
canvas: tk.Canvas
window_width: int = 700
window_height: int = 500
FPS: int = 30
interval: int = int(1000/FPS) # Since .after(ms: int) is in milliseconds

# System input variables
mouse_x: int = 0
mouse_y: int = 0

# System functionality variables
state: int = 1
bg: display.Bg

# Entry point
def main():
    global root, canvas, window_width, window_height

    # setting up window
    root = tk.Tk()
    root.title("Nav")
    root.resizable(False, False)

    # setting up a canvas
    canvas = tk.Canvas(root, width = window_width, height = window_height, bg = "Gray")
    canvas.pack()

    # Bind add events' callback
    canvas.bind("<Motion>", on_motion)

    init()
    update(root)
    root.mainloop() # run once, keep thread alive, waiting for callbacks and events until window closed

# Main loop
def update(root: tk.Tk):
    '''update function'''
    global state, canvas, bg

    match state:
        case 1:
            '''user input'''
            canvas.delete("hud")
            bg.update(canvas)
            canvas.create_text(mouse_x, mouse_y, text = "龙", fill = "black", tags = "hud")
        case 2:
            '''generate plan'''
        case 3:
            '''execution'''
        case 4:
            '''next step'''
        case 0:
            return

    print(f'x:{mouse_x},y:{mouse_y}')# DEBUG
    root.after(interval, update, root) # put update() on wait while utilising main thread for others

def init():
    '''initialise variables'''
    global bg, canvas, window_width, window_height
    bg = display.Bg(canvas, x = window_width/2, y = window_height/2, r = 10)

def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y

main()