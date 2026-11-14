import tkinter as tk

# System setup variables
FPS = 10
interval = int(1000/FPS) # Since .after(ms: int) is in milliseconds

# System input variables
mouse_x, mouse_y = 0, 0

# Entry point
def main():
    # setting up window
    root = tk.Tk()
    root.title("Nav")
    root.resizable(False, False)

    # setting up a canvas
    window_width, window_height = 700, 500
    canvas = tk.Canvas(root, width = window_width, height = window_height, bg = "Black")
    canvas.pack()

    # Bind add events' callback
    canvas.bind("<Motion>", on_motion)

    update(root)
    root.mainloop() # run once, keep thread alive, waiting for callbacks and events until window closed

# Main loop
def update(root: tk.Tk):
    '''update function'''
    print(f'x:{mouse_x},y:{mouse_y}')# DEBUG
    root.after(interval, update, root) # put update() on wait while utilising main thread for others

def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y


main()