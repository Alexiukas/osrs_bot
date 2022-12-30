import sys
import customtkinter
from available_scritps_frame import AvailableScriptsFrame
from dictionary import scripts, action_list
from file_worker import load_scripts
from home_frame import HomeFrame
from script_setup_frame import ScriptSetupFrame
from mouse_frame import MouseFrame

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


def clear_frame(items):
    for item in items:
        item.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("660x440")
        load_scripts()
        self.resizable(False, False)
        self.title("The Bachelor Bot")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.selected_script = None
        self.is_following_rs = False
        self.mouse_values = None
        self.font = customtkinter.CTkFont(weight="bold")

        self.frame_left = customtkinter.CTkFrame(self)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_left.grid_rowconfigure(4, weight=1)

        self.frame_right = customtkinter.CTkFrame(self)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame_left.home_button = customtkinter.CTkButton(master=self.frame_left, font=self.font, corner_radius=20, height=40, border_spacing=10, text="Home", command=self.open_home_view, anchor="w")
        self.frame_left.home_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.frame_left.scripts_button = customtkinter.CTkButton(master=self.frame_left,font=self.font, corner_radius=20, height=40, border_spacing=10, text="Scripts", command=self.open_scripts_view, anchor="w")
        self.frame_left.scripts_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.frame_left.mouse_button = customtkinter.CTkButton(master=self.frame_left,font=self.font, corner_radius=20, height=40, border_spacing=10, text="Mouse configuration", command=self.open_mouse_view, anchor="w")
        self.frame_left.mouse_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.frame_left.exit_button = customtkinter.CTkButton(master=self.frame_left, font=self.font, corner_radius=20, height=40, border_spacing=10, text="Exit", command=sys.exit)
        self.frame_left.exit_button.grid(row=5, column=0, padx=20, pady=20, sticky="s")

    def open_scripts_view(self):
        clear_frame(self.frame_right.winfo_children())
        AvailableScriptsFrame(self.frame_right, scripts=scripts, update=self.script_setup_frame)

    def open_home_view(self):
        clear_frame(self.frame_right.winfo_children())
        HomeFrame(self.frame_right, script_selected=self.selected_script, main_button_switch=self.switch_buttons, mouse_settings=self.mouse_values)

    def script_setup_frame(self, text):
        clear_frame(self.frame_right.winfo_children())
        ScriptSetupFrame(self.frame_right, header=text, actions=action_list[text], save_script=self.save_selected_script)

    def save_selected_script(self, script):
        self.selected_script = script

    def switch_buttons(self, disable):
        self.frame_left.home_button.configure(state="disabled" if disable else "normal")
        self.frame_left.scripts_button.configure(state="disabled" if disable else "normal")
        self.frame_left.mouse_button.configure(state="disabled" if disable else "normal")

    def open_mouse_view(self):
        clear_frame(self.frame_right.winfo_children())
        MouseFrame(self.frame_right, mouse_settings=self.save_mouse_settings)

    def save_mouse_settings(self, G, W, M):
        self.mouse_values = [G, W, M]


if __name__ == "__main__":
    app = App()
    app.mainloop()
