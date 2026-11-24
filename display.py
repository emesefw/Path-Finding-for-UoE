import tkinter as tk
import handler
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # terminal: python3 -m pip install pillow (for macOS), python -m pip install pillow (for windows)

fh = handler.FileHandler()

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
        self.window_width = window_width
        self.window_height = window_height

    def rescale(self, file_path: str, scalling_command: str = "original", scalling_bias: float = 0) -> ImageTk.PhotoImage:
        scale: float
        new_size: tuple
        image = Image.open(file_path)
        
        match(scalling_command):
            case "width":
                scale = self.window_width / image.width
            case "height":
                scale = self.window_height / image.height
            case "both":
                scale = max(self.window_width / image.width, self.window_height / image.height) # always make image takes up whole window
            case "original":
                scale = 1
            
        new_size = (int(image.width * scale * (1 + scalling_bias)), int(image.height * scale * (1 + scalling_bias)))
        image = image.resize(new_size, Image.Resampling.LANCZOS) # Resampling.NEAREST, Resampling.BOX, Resampling.BILINEAR, Resampling.HAMMING, Resampling.BICUBIC, Resampling.LANCZOS, Resampling.MKS2013, or Resampling.MKS2021
        image_out = ImageTk.PhotoImage(image)

        print(f'{scalling_command} is multiplied by sf: {scale}')
        return image_out

    def find_center(self, image_width, image_height) -> tuple:
        return ((self.window_width / 2) - (image_width / 2), (self.window_height / 2) - (image_height / 2))

class Menu(Display):
    global fh

    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        self.default_text = [["BUILDING you are in","FLOOR you are on","ROOM you are in"],["destination BUILDING","destination FLOOR","destination ROOM"]]
        self.user_input: list = self.default_text # array of 2 rows and 3 coloums
        self.list_o: list = [[],[],[]]
        self.list_d: list = [[],[],[]]
        self.end_state = False

        self.logo_image = self.rescale("res/image/menu/Uni-logo-EDINBURGH_730x290.png", "original")
        self.logo_image_id = canvas.create_image(320, 110, image = self.logo_image)

        self.origin: list = [0,0,0] # actual boxes for origin
        self.destination: list = [0,0,0] # actual boxes for destination

        self.origin[0] = ttk.Combobox(state = "readonly", values = self.list_o[0]) # Read from file to optain all options and create a list
        self.origin[1] = ttk.Combobox(state = "readonly", values = self.list_o[1])
        self.origin[2] = ttk.Combobox(state = "readonly", values = self.list_o[2])
        self.destination[0] = ttk.Combobox(state = "readonly", values = self.list_d[0])
        self.destination[1] = ttk.Combobox(state = "readonly", values = self.list_d[1])
        self.destination[2] = ttk.Combobox(state = "readonly", values = self.list_d[2])

        self.origin[0].bind("<<ComboboxSelected>>", self.on_selection_o_0)
        self.origin[1].bind("<<ComboboxSelected>>", self.on_selection_o_1)
        self.destination[0].bind("<<ComboboxSelected>>", self.on_selection_d_0)
        self.destination[1].bind("<<ComboboxSelected>>", self.on_selection_d_1)

        self.go_button = ttk.Button(text = "Go",  command = self.pressed)
        self.clear_button = ttk.Button(text = "Clear all", command = self.clear_all)

        self.clear_all()
        self.show(canvas, window_width, window_height)

    def update(self):
        '''combine the list here'''
        self.list_o[0] = fh.read_list(field=0, choice=0, reference=self.user_input)
        self.list_o[1] = fh.read_list(field=1, choice=0, reference=self.user_input)
        self.list_o[2] = fh.read_list(field=2, choice=0, reference=self.user_input)

        self.origin[0].configure(values=self.list_o[0])
        self.origin[1].configure(values=self.list_o[1])
        self.origin[2].configure(values=self.list_o[2])

        self.list_d[0] = fh.read_list(field=0, choice=1, reference=self.user_input)
        self.list_d[1] = fh.read_list(field=1, choice=1, reference=self.user_input)
        self.list_d[2] = fh.read_list(field=2, choice=1, reference=self.user_input)

        self.destination[0].configure(values=self.list_d[0])
        self.destination[1].configure(values=self.list_d[1])
        self.destination[2].configure(values=self.list_d[2])

    def read_input(self):
        self.user_input = [[self.origin[0].get(), self.origin[1].get(), self.origin[2].get()],[self.destination[0].get(), self.destination[1].get(), self.destination[2].get()]]

    def on_selection_o_0(self, event):
        self.origin[1].set(self.default_text[0][1])
        self.origin[2].set(self.default_text[0][2])

    def on_selection_o_1(self, event):
        self.origin[2].set(self.default_text[0][2])

    def on_selection_d_0(self, event):
        self.destination[1].set(self.default_text[1][1])
        self.destination[2].set(self.default_text[1][2])
        
    def on_selection_d_1(self, event):
        self.destination[2].set(self.default_text[1][2])

    def clear_all(self):
        self.origin[0].set(self.default_text[0][0])
        self.origin[1].set(self.default_text[0][1])
        self.origin[2].set(self.default_text[0][2])
        self.destination[0].set(self.default_text[1][0])
        self.destination[1].set(self.default_text[1][1])
        self.destination[2].set(self.default_text[1][2])
    
    def pressed(self):
        if self.user_input[0][0] == self.default_text[0][0] or self.user_input[0][1] == self.default_text[0][1] or self.user_input[0][2] == self.default_text[0][2] or self.user_input[1][0] == self.default_text[1][0] or self.user_input[1][1] == self.default_text[1][1] or self.user_input[1][2] == self.default_text[1][2]:
            print(self.user_input) # DEBUG
            messagebox.showinfo(title = "Error message -_-'", message = "please enter all the fields required: \n(building, floor, room)")
            self.end_state =  False
        else:
            self.end_state = True
        
    def hide(self, canvas: tk.Canvas):
        canvas.itemconfig(self.logo_image_id, state = "hidden")

        self.origin[0].place_forget()
        self.origin[1].place_forget()
        self.origin[2].place_forget()
        self.destination[0].place_forget()
        self.destination[1].place_forget()
        self.destination[2].place_forget()
        self.go_button.place_forget()
        self.clear_button.place_forget()

    def show(self, canvas: tk.Canvas, window_width: int, window_height: int):
        off_x: int = 10
        off_y: int = 100
        splitting_factor_x: int = 5
        splitting_factor_y: int = 5

        canvas.itemconfig(self.logo_image_id, state = "normal")

        self.origin[0].place(x = off_x, y = int(1 * window_height/splitting_factor_y) + off_y)
        self.origin[1].place(x = int(1 * window_width/splitting_factor_x) + off_x, y = int(1 * window_height/splitting_factor_y) + off_y)
        self.origin[2].place(x = int(2 * window_width/splitting_factor_x) + off_x, y = int(1 * window_height/splitting_factor_y) + off_y)
        self.destination[0].place(x = off_x, y = int(2 * window_height/splitting_factor_y) + off_y)
        self.destination[1].place(x = int(1 * window_width/splitting_factor_x) + off_x, y = int(2 * window_height/splitting_factor_y) + off_y)
        self.destination[2].place(x = int(2 * window_width/splitting_factor_x) + off_x, y = int(2 * window_height/splitting_factor_y) + off_y)

        self.go_button.place(x = int(3 * window_width/splitting_factor_x) + off_x, y = int(2 * window_height/splitting_factor_y) + off_y)
        self.clear_button.place(x = off_x, y = int(3 * window_height/splitting_factor_y) + off_y)

class Projector(Display):
    def __init__(self, canvas: tk.Canvas, window_width: int, window_height: int):
        super().__init__(window_width, window_height)
        self.image_x_coor: int = 0
        self.image_y_coor: int = 0
        self.image_r_edge: int = 0

        self.test_image: ImageTk.PhotoImage
        self.test_image_back: ImageTk.PhotoImage
        self.test_image_back_id = canvas.create_image(self.image_x_coor, self.image_y_coor, anchor = "nw")
        self.test_image_id = canvas.create_image(self.image_x_coor, self.image_y_coor, anchor = "nw")

        self.image_file_icon = tk.PhotoImage(file = "res/image/menu/pc-portrait-red.png") # FUN
        self.icon_image_id = canvas.create_image(int(window_width/2), int(window_height/2), image = self.image_file_icon)

    def update(self, canvas: tk.Canvas, x : int, y: int):
        canvas.coords(self.icon_image_id, x, y)
        #canvas.coords(self.test_image_id, x, y)

        self.wraprojector(canvas, Image.open("res/image/panorama/test.png"), x, 0.75)
        canvas.coords(self.test_image_back_id, self.image_r_edge, self.image_y_coor)


    def wraprojector(self, canvas: tk.Canvas, original: Image.ImageFile, off_l = 0, bias: float = 1):
        ratio = self.window_height / original.height # 900 / 200 = 4
        frame_width = int(self.window_width / ratio) # 1200 / 4 = 300

        off_l = off_l % original.width
        off_r = min(off_l + frame_width, original.width)
        frame_1 = (off_l, 0, min(off_l + frame_width, original.width), original.height)
        frame_2_width = abs(off_l + frame_width - original.width)
        frame_2 = (0, 0, frame_2_width, original.height)

        crop: Image = original.crop(frame_1) # left, top, right, bottom
        crop = crop.resize((int(min(self.window_width, ratio * (off_r - off_l)) * bias), int(self.window_height * bias)), Image.LANCZOS)
        self.test_image = ImageTk.PhotoImage(crop)
        canvas.itemconfig(self.test_image_id, image = self.test_image)

        image_width = ratio * bias * frame_width
        image_2_width = image_width - (ratio * (off_r - off_l) * bias)
        if frame_2_width > 0:
            crop = original.crop(frame_2)
            crop = crop.resize((max(1, int(image_2_width)), int(self.window_height * bias)), Image.LANCZOS)
            self.test_image_back = ImageTk.PhotoImage(crop)
            canvas.itemconfig(self.test_image_back_id, image = self.test_image_back)

            self.image_r_edge = int(image_width - image_2_width) + self.image_x_coor

    def hide(self, canvas: tk.Canvas):
        canvas.itemconfig(self.test_image_id, state = "hidden")
        canvas.itemconfig(self.test_image_back_id, state = "hidden")
        canvas.itemconfig(self.icon_image_id, state = "hidden")

    def show(self, canvas: tk.Canvas):
        canvas.itemconfig(self.test_image_id, state = "normal")
        canvas.itemconfig(self.test_image_back_id, state = "normal")
        #canvas.itemconfig(self.icon_image_id, state = "normal")

