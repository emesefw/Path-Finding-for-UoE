import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # terminal: python3 -m pip install pillow (for macOS), python -m pip install pillow (for windows)

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

    def rescale(self, file_path: str, scalling_command: str = "original", scalling_bias: float = 0) -> ImageTk.PhotoImage:
        scale: float
        new_size: tuple

        image = Image.open(file_path)
        
        match(scalling_command):
            case "width":
                self.window_width / image.width
            case "height":
                scale = self.window_height / image.height
            case "both":
                scale = min(self.window_width / image.width, self.window_height / image.height)
            case "original":
                scale = 1

        new_size = (int(image.width * scale * (1 + scalling_bias)), int(image.height * scale * (1 + scalling_bias)))
        image = image.resize(new_size, Image.LANCZOS) # Resampling.NEAREST, Resampling.BOX, Resampling.BILINEAR, Resampling.HAMMING, Resampling.BICUBIC, Resampling.LANCZOS, Resampling.MKS2013, or Resampling.MKS2021
        image_out = ImageTk.PhotoImage(image)

        print(f'{scalling_command} is multiplied by sf: {scale}')
        return image_out

class Menu(Display):
    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        self.choice: list = ["","",""]
        self.end_state = False

        image_file = tk.PhotoImage(file = "res/image/menu/Uni-logo-EDINBURGH_730x290.png")
        #self.image_scaled = self.resize(image = image_file, scale_reference = "width", image_width = image_file.width(), image_height = image_file.height(), scalling_bias = -0.5)
        self.image_scaled = self.rescale("res/image/menu/Uni-logo-EDINBURGH_730x290.png", "original")
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
        self.image_scaled = self.rescale("res/image/panorama/test.png", "height") # DEBUG

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

