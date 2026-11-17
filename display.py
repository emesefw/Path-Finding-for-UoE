import tkinter as tk
from tkinter import ttk, messagebox

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

    def resize(self, image: tk.PhotoImage, image_width: int, image_height: int, sf: float = 1, scalling_bias: float = 0):
        '''resize image to screen resolution'''
        flag: bool = False
        x_difference: int = 0
        y_difference: int = 0
        largest_difference: int
        scalling_factor: float

        if image_width > self.window_width: # case width of image > width of window
            x_difference = image_width - self.window_width
            flag = True
        if image_height > self.window_height: # case height of image > that of the window
            y_difference = image_height - self.window_height
            flag = True

        if flag == True:
            if x_difference > y_difference: # work out the larger difference
                largest_difference = x_difference
                scalling_factor = 1 - largest_difference/image_width # find the multiplying factor to original image
            else:
                largest_difference = y_difference
                scalling_factor = 1 - largest_difference/image_height
            if sf != 1 and round(sf, 1) != 0:
                scalling_factor = round(sf * (1 + scalling_bias), 1)
            else:
                scalling_factor = round(scalling_factor * (1 + scalling_bias), 1) # round to 1 decimal place
            return image.zoom(int(scalling_factor * 10)).subsample(10)
        
        else:
            return image # no change to image

class Menu(Display):
    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        self.choice: list = ["","",""]
        self.end_state = False

        self.image_file = tk.PhotoImage(file = "res/image/Uni-logo-EDINBURGH_730x290.png")
        self.image_display = canvas.create_image(320, 110, image = self.image_file)

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
