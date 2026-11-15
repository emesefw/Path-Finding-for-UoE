import tkinter as tk

# System setup variables
window_width: int = 700
window_height: int = 500
FPS: int = 10
interval: int = int(1000/FPS) # Since .after(ms: int) is in milliseconds

# System input variables
mouse_x: int = 0
mouse_y: int = 0

# System functionality variables
state: int = 1

# Entry point
def main():
    # Initialise all veriables
    init()

    # setting up window
    root = tk.Tk()
    root.title("Nav")
    root.resizable(False, False)

    # setting up a canvas
    global window_width, window_height
    canvas = tk.Canvas(root, width = window_width, height = window_height, bg = "Black")
    canvas.pack()

    # Bind add events' callback
    canvas.bind("<Motion>", on_motion)

    update(root)
    root.mainloop() # run once, keep thread alive, waiting for callbacks and events until window closed

# Main loop
def update(root: tk.Tk):
    '''update function'''
    global state

    match state:
        case 1:
            '''user input'''
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

def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y

main()