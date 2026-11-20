import tkinter as tk
import display

# System setup variables
root: tk.Tk
canvas: tk.Canvas
window_scale_factor: int = 90
window_width: int = 16 * window_scale_factor
window_height: int = 9 * window_scale_factor
FPS: int = 30
interval: int = int(1000/FPS) # Since .after(ms: int) is in milliseconds

# System input variables
mouse_x: int = 0
mouse_y: int = 0

# System functionality variables
state: int = 1
menu: display.Menu
projector: display.Projector

# Entry point
def main():
    global root, canvas, window_width, window_height

    # setting up window
    root = tk.Tk()
    root.title("Nav")
    root.resizable(False, False)

    # setting up a canvas
    canvas = tk.Canvas(root, width = window_width, height = window_height, bg = "white")
    canvas.pack()

    # Bind add events' callback
    canvas.bind("<Motion>", on_motion)
    canvas.bind("<Button>", on_mouse_clicked)

    init()
    update(root)
    root.mainloop() # run once, keep thread alive, waiting for callbacks and events until window closed

def update(root: tk.Tk):
    '''update function'''
    global state, canvas

    match state:
        case 1:
            '''user input'''
            canvas.delete("hud") # DEBUG
            canvas.create_text(mouse_x, mouse_y, text = f'x:{mouse_x}, y:{mouse_y}', fill = "black", tags = "hud") # DEBUG

            menu.show(canvas, window_width, window_height)
            menu.read_input() # check for user input
            if menu.end_state == True:
                state = 3
                menu.hide(canvas) # hide the menu from previous state
        case 2:
            '''generate plan'''
            print("state 2")
        case 3:
            '''execution'''
            #print("state 3") # DEBUG
            projector.show(canvas)
            projector.update(canvas, mouse_x, mouse_y)
        case 4:
            '''next step'''
        case 0:
            root.destroy()

    #print(f'x:{mouse_x},y:{mouse_y}')# DEBUG
    root.after(interval, update, root) # put update() on wait while utilising main thread for others

def init():
    '''initialise variables'''
    global canvas, window_width, window_width, menu, projector

    menu = display.Menu(canvas, window_width, window_height)
    projector = display.Projector(canvas, window_width, window_height)
    menu.hide(canvas)
    projector.hide(canvas)

def on_motion(event):
    global mouse_x, mouse_y
    
    mouse_x = event.x
    mouse_y = event.y

def on_mouse_clicked(event):
    '''pass event.x and event.y as parameters to methods'''

main()