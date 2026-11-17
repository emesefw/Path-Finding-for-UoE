import tkinter as tk
from tkinter import ttk, messagebox
import time # BEGUD

class Bg: # testing class
    def __init__(self, canvas: tk.Canvas, x: int = 0, y: int = 0, r: float = 100):
        self.x = x
        self.y = y
        self.r = r
        self.image = canvas.create_oval(
            x - r, y - r, 
            x + r, y + r,
            fill = "White", width = 0
        )

    def update(self, canvas: tk.Canvas):
        canvas.coords(
            self.image,
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r
        )

class Display:
    def __init__(self, window_width: int, window_height: int):
        ''''''
        self.window_width = window_width
        self.window_height = window_height

    def resize(self, image: tk.PhotoImage, image_width: int = 0, image_height: int = 0, scale_reference: str = "none", sf: float = 1, scalling_bias: float = 0):
        '''resize image to screen resolution'''
        flag: bool = False
        x_difference: int = 0
        y_difference: int = 0
        largest_difference: int
        scalling_factor: float
        
        match(scale_reference):
            case "none": # case where neither side is prefered
                if image_width > self.window_width: # case width of image > width of window
                    x_difference = image_width - self.window_width
                    flag = True
                if image_height > self.window_height: # case height of image > that of the window
                    y_difference = image_height - self.window_height
                    flag = True
            case "width":
                x_difference = image_width - self.window_width
                flag = True
            case "height":
                y_difference = image_height - self.window_height
                flag = True

        if flag == True:
            match(scale_reference):
                case "none": # case where neither side is prefered
                    if x_difference > y_difference: # work out the larger difference
                        largest_difference = x_difference
                        scalling_factor = 1 - largest_difference/image_width # find the multiplying factor to original image
                    else:
                        largest_difference = y_difference
                        scalling_factor = 1 - largest_difference/image_height
                case "width":
                    largest_difference = x_difference
                    scalling_factor = 1 - largest_difference/image_width
                case "height":
                    largest_difference = y_difference
                    scalling_factor = 1 - largest_difference/image_height

            if sf != 1 and round(sf, 1) != 0:
                scalling_factor = round(sf * (1 + scalling_bias), 1)
            else:
                scalling_factor = round(scalling_factor * (1 + scalling_bias), 1) # round to 1 decimal place

            print(f"return scaled image, sf:{scalling_factor}") # DEBUG
                
            return image.zoom(int(scalling_factor * 10)).subsample(10)
        
        else:
            print("not scaled") # DEBUG
            return image # no change to image

    def rescale(self, image: tk.PhotoImage, scalling_side: str = "none", scalling_bias: float = 0) -> tk.PhotoImage:
        sf: float
        
        match(scalling_side):
            case "width":
                diff = image.width() - self.window_width
                sf = 1 - diff / image.width()
            case "height":
                diff = image.height() - self.window_height
                sf = 1 - diff / image.height()
            case "none":
                print("failed to scale, choose a either 'width' or 'height'.")
                return image

        sf = round(sf * (1 + scalling_bias), 1)
        print(f'{scalling_side} is multiplied by sf: {sf}')
        return image.zoom(int(sf * 10)).subsample(10)



class Menu(Display):
    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        self.choice: list = ["","",""]
        self.end_state = False

        image_file = tk.PhotoImage(file = "res/image/menu/Uni-logo-EDINBURGH_730x290.png")
        #self.image_scaled = self.resize(image = image_file, scale_reference = "width", image_width = image_file.width(), image_height = image_file.height(), scalling_bias = -0.5)
        self.image_scaled = self.rescale(image_file, "none")
        self.image_display = canvas.create_image(320, 110, image = self.image_scaled)

        self.building = ttk.Combobox(
            state = "readonly",
            values = ["load","all","options","here"] # Read from file to optain all options and create a list
        )
        self.floor = ttk.Combobox(
            state = "readonly",
            values = ["load","all","options","here"] # Read from file to optain all options and create a list
        )
        self.room = ttk.Combobox(
            state = "readonly",
            values = ["load","all","options","here"] # Read from file to optain all options and create a list
        )
        self.next_button = ttk.Button(
            text = "Go",
            command = self.pressed
        )

        self.show(canvas, window_width, window_height)

    def selection(self):
        '''output choices'''
        self.choice = [self.building.get(), self.floor.get(), self.room.get()]
        #print(self.choice) # DEBUG
    
    def pressed(self):
        '''update state if pressed go in correct condition'''
        if self.choice[0] == "" or self.choice[1] == "" or self.choice[2] == "":
            messagebox.showinfo(title = "Error message -_-'", message = "please enter all the fields required: \n(building, floor, room)")
            self.end_state =  False
        else:
            self.end_state = True
        
    def hide(self, canvas: tk.Canvas):
        canvas.itemconfig(self.image_display, state = "hidden")

        self.building.place_forget()
        self.floor.place_forget()
        self.room.place_forget()
        self.next_button.place_forget()

    def show(self, canvas: tk.Canvas, window_width: int, window_height: int):
        margin: int = 10
        splitting_factor_x: int = 4
        splitting_factor_y: int = 4

        canvas.itemconfig(self.image_display, state = "normal")

        self.building.place(x = margin, y = int(1 * window_height/splitting_factor_y))
        self.floor.place(x = int(1 * window_width/splitting_factor_x) + margin, y = int(1 * window_height/splitting_factor_y))
        self.room.place(x = int(2 * window_width/splitting_factor_x) + margin, y = int(1 * window_height/splitting_factor_y))
        self.next_button.place(x = int(3 * window_width/splitting_factor_x) + margin, y = int(1 * window_height/splitting_factor_y))

class Projector(Display):
    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        #print("start to initialise projector") # DEBUG

        self.image_list: list # list of imaged pre loaded before execution
        image_file = tk.PhotoImage(file = "res/image/panorama/test.png") # DEBUG
        self.image_file_icon = tk.PhotoImage(file = "res/image/menu/pc-portrait-red.png")

        #print("is it here that takes long?") # DEBUG

        #image_scaled = self.resize(image = image_file, scale_reference = "height", image_height = image_file.height(), scalling_bias = 0.5) # DEBUG
        self.image_scaled = self.rescale(image_file, "height", -0.7) # DEBUG

        #print("or perhaps the resize method?") # DEBUG

        #self.image_projected = canvas.create_image(int(window_width/2), int(window_height/2), image = image_scaled) # in real thing append into list
        self.image_projected = canvas.create_image(int(window_width/2), int(window_height/2), image = self.image_scaled)
        self.image_projected_icon = canvas.create_image(int(window_width/2), int(window_height/2), image = self.image_file_icon)

        #print("projecter initialised") # DEBUG

    def update(self, canvas: tk.Canvas, x : int, y: int):
        canvas.coords(self.image_projected_icon, x, y)

    def hide(self, canvas: tk.Canvas):
        canvas.itemconfig(self.image_projected, state = "hidden")
        canvas.itemconfig(self.image_projected_icon, state = "hidden")

    def show(self, canvas: tk.Canvas):
        canvas.itemconfig(self.image_projected, state = "normal")
        canvas.itemconfig(self.image_projected_icon, state = "normal")

