import customtkinter
import dictionary
import utilities


class ScriptSetupFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header: str, actions, save_script, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(4, weight=1)
        self.columnconfigure(3, weight=1)
        self.header_text = header
        self.save = save_script

        # Header
        self.header = customtkinter.CTkLabel(self, text=header + " script", font=customtkinter.CTkFont(size=15, weight="bold"), anchor="w")
        self.header.grid(row=0, column=1, padx=10, pady=10)

        # first row
        self.timer_label = customtkinter.CTkLabel(self, text="How long should bot run?")
        self.timer_label.grid(row=1, column=0, padx=10, pady=10)

        self.slider = customtkinter.CTkSlider(master=self, from_=15, to=180, number_of_steps=12, command=lambda x: self.slider_event(x))
        self.slider.set(15)
        self.slider.grid(row=1, column=1, padx=10, pady=10)

        self.timer_value = customtkinter.CTkLabel(self, text=str(int(self.slider.get())))
        self.timer_value.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # second row
        self.drop_label = customtkinter.CTkLabel(self, text="drop items?" if "Combat" not in header else "Select food:")
        self.drop_label.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        if "Combat" not in header:
            self.drop_check = customtkinter.CTkCheckBox(self, text="", onvalue="Yes", offvalue="No")
        else:
            self.drop_check = customtkinter.CTkOptionMenu(self, values=['shrimp', 'meat', 'trout/salmon'])

        self.drop_check.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # third row
        self.action_label = customtkinter.CTkLabel(self, text="Select action:")
        self.action_label.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.action_options = customtkinter.CTkOptionMenu(self, values=actions)
        self.action_options.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_event)
        self.save_button.grid(row=4, column=1, stick="s", padx=10, pady=10)

    def save_event(self):
        time = int(self.slider.get())
        drop = self.drop_check.get()
        action = self.action_options.get()
        name = self.header.cget("text")
        after_action_wait = False if "Mining" in name or "tree" in action else True

        script_selected = {"name": name, "run_time": time, "item": drop, "action": action, "bot_type": dictionary.bot_type.get(self.header_text), "wait": after_action_wait}
        self.save(script_selected)

    def slider_event(self, x):
        self.timer_value.configure(text=str(int(x)))
