import tkinter as tk
import display

# System setup variables
root: tk.Tk
canvas: tk.Canvas
window_width: int = 1024
window_height: int = 512
FPS: int = 10
interval: int = int(1000/FPS) # Since .after(ms: int) is in milliseconds

# System input variables
mouse_x: int = 0
mouse_y: int = 0

# System functionality variables
state: int = 1
bg: display.Bg
menu: display.Menu

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
    canvas.bind("<Button>", on_mouse_clicked)

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
            canvas.create_text(mouse_x, mouse_y, text = "", fill = "black", tags = "hud")
            
            menu.selection() # check for user input
            if menu.end_state == True:
                state = 2
                menu.hide() # hide the menu from previous state
        case 2:
            '''generate plan'''
            print("state 2")
        case 3:
            '''execution'''
        case 4:
            '''next step'''
        case 0:
            root.destroy()

    print(f'x:{mouse_x},y:{mouse_y}')# DEBUG
    root.after(interval, update, root) # put update() on wait while utilising main thread for others

def init():
    '''initialise variables'''
    global bg, canvas, window_width, window_width, menu
    bg = display.Bg(canvas, x = window_width/2, y = window_height/2, r = 10)
    menu = display.Menu(window_width, window_height)

def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y

def on_mouse_clicked(event):
    '''pass event.x and event.y as parameters to methods'''

main()