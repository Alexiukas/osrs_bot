import customtkinter


class AvailableScriptsFrame(customtkinter.CTkFrame):
    def __init__(self, *args, scripts, update, **kwargs):
        super().__init__(*args, **kwargs)
        self.update = update
        self.grid(row=0, column=0, sticky="nsew")

        self.private_label = customtkinter.CTkLabel(self, text="Available scripts:", font=customtkinter.CTkFont(size=15, weight="bold"))
        index = 0

        for script in scripts:
            button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, fg_color="transparent", text_color=("gray10", "gray90"), text=script,
                                             hover_color=("gray70", "gray30"), anchor="w")
            button.configure(command=lambda x=script: self.open_script_setup_view(x))
            button.grid(row=index, column=0, sticky="ew", padx=10, pady=1)
            index += 1

    def open_script_setup_view(self, text):
        self.update(text)
