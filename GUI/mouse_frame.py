import math
import threading
import time
import tkinter
import customtkinter
import win32gui
import pyautogui
import mouse_mover


colors = ['red', 'green', 'blue', 'cyan', 'orange', 'purple', 'brown', 'pink', 'magenta', 'black']
global index


class MouseFrame(customtkinter.CTkFrame):
    def __init__(self, *args, mouse_settings, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(4, weight=1)
        self.columnconfigure(3, weight=1)
        self.save_mouse = mouse_settings

        # Header
        self.header = customtkinter.CTkLabel(self, text="Mouse algorithm setup", font=customtkinter.CTkFont(size=15, weight="bold"), anchor="w")
        self.header.grid(row=0, column=1, padx=10, pady=10)

        self.gravity_label = customtkinter.CTkLabel(self, text="Gravity force")
        self.gravity_label.grid(row=1, column=0, padx=10, pady=10)

        self.gravity_slider = customtkinter.CTkSlider(master=self, from_=1, to=5, number_of_steps=4, command=lambda x: self.gravity_value.configure(text=str(int(x))))
        self.gravity_slider.set(1)
        self.gravity_slider.grid(row=1, column=1, padx=10, pady=10)

        self.gravity_value = customtkinter.CTkLabel(self, text=str(int(self.gravity_slider.get())))
        self.gravity_value.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.wind_label = customtkinter.CTkLabel(self, text="Wind force")
        self.wind_label.grid(row=2, column=0, padx=10, pady=10)

        self.wind_slider = customtkinter.CTkSlider(master=self, from_=1, to=5, number_of_steps=4, command=lambda x: self.wind_value.configure(text=str(int(x))))
        self.wind_slider.set(1)
        self.wind_slider.grid(row=2, column=1, padx=10, pady=10)

        self.wind_value = customtkinter.CTkLabel(self, text=str(int(self.wind_slider.get())))
        self.wind_value.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        self.steps_label = customtkinter.CTkLabel(self, text="Step size")
        self.steps_label.grid(row=3, column=0, padx=10, pady=10)

        self.steps_slider = customtkinter.CTkSlider(master=self, from_=1, to=10, number_of_steps=9, command=lambda x: self.steps_value.configure(text=str(int(x))))
        self.steps_slider.set(1)
        self.steps_slider.grid(row=3, column=1, padx=10, pady=10)

        self.steps_value = customtkinter.CTkLabel(self, text=str(int(self.steps_slider.get())))
        self.steps_value.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)

        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_event)
        self.save_button.grid(row=7, column=1, stick="s", padx=10, pady=10)

        self.test_button = customtkinter.CTkButton(self, text="Test", command=self.test_event)
        self.test_button.grid(row=6, column=1, stick="s", padx=10, pady=10)

    def save_event(self):
        self.G = math.floor(self.gravity_slider.get()) + 3
        self.W = math.floor(self.wind_slider.get())
        self.M = math.floor(self.steps_slider.get()) + 10

        self.save_mouse(self.G, self.W, self.M)

    def paint(self, event):
        global lasx, lasy, index
        self.canvas.create_line((lasx, lasy, event.x, event.y), fill=colors[index], width=2)
        lasx, lasy = event.x, event.y

    def get_x_and_y(self, event):
        global lasx, lasy
        lasx, lasy = event.x, event.y

    def test_event(self):
        self.save_event()
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x500")
        window.title("Mouse test")

        # create label on CTkToplevel window
        self.canvas = tkinter.Canvas(window, bg='white', height=500, width=600)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-1>', self.get_x_and_y)
        self.canvas.pack()

        threading.Thread(target=self.move_mouse).start()

    def move_mouse(self):
        global index
        index = 0
        canvas_y = 100
        time.sleep(.75)
        canvas = win32gui.FindWindow(None, "Mouse test")
        coordinates = list(win32gui.GetWindowRect(canvas))

        mm = mouse_mover.WindMouse(self.G, self.W, self.M)

        for i in range(10):
            pyautogui.moveTo(coordinates[0] + 50, coordinates[1] + canvas_y)
            x, y = pyautogui.position()
            mm.wind_mouse(x, y, x + 500, y, drag=True)
            index += 1
            canvas_y += 40

        index = 0
        self.canvas.configure(state='disabled')
