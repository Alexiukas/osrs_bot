from datetime import datetime as dt
import tkinter as tk
import customtkinter as ct
import threading
import file_worker
import mouse_mover
import combat_bot
import gathering_bot
import time
import utilities


class HomeFrame(ct.CTkFrame):
    def __init__(self, *args, script_selected, main_button_switch, mouse_settings, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.script = script_selected
        self.main_button_switch = main_button_switch
        self.header = ct.CTkLabel(self, text= "First select script to run" if script_selected is None else script_selected["name"])
        self.header.grid(row=0, column=1, padx=10, pady=10)
        self.is_running = False
        self.is_paused = False
        self.mouse_settings = mouse_settings# mouse_mover.WindMouse(mouse_settings[0], mouse_settings[1], mouse_settings[2]) if mouse_settings is not None else mouse_mover.WindMouse
        self.start_time = 0

        self.start_button = ct.CTkButton(self, text="START", corner_radius=15, height=20, width=80, border_spacing=10, command=self.start, state="disabled" if script_selected is None else "normal")
        self.start_button.grid(row=1, column=0, padx=5, pady=5)
        self.pause_button = ct.CTkButton(self, text="PAUSE", corner_radius=15, height=20, width=80, border_spacing=10, state="disabled", command=self.pause)
        self.pause_button.grid(row=1, column=1, padx=5, pady=5)
        self.stop_button = ct.CTkButton(self, text="STOP", corner_radius=15, height=20, width=80, border_spacing=10, state="disabled", command=self.stop)
        self.stop_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_log = ct.CTkCheckBox(self, text="Save logs after finishing?")
        self.save_log.grid(row=2, column=1, padx=10, pady=10)

        self.log_box = ct.CTkTextbox(self, width=400, state="disabled")
        self.log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="s")

        self.run_time_label = ct.CTkLabel(self, text="")
        self.run_time_label_text = ct.CTkLabel(self, text="Total run time:")
        self.loot_count_label = ct.CTkLabel(self, text="")
        self.loot_count_label_text = ct.CTkLabel(self, text="Total kill count:" if script_selected is not None and 'local' in script_selected['bot_type'] else "Total loot count:")
        self.run_time_label.grid(row=4, column=1, padx=10, pady=2, sticky="w")
        self.run_time_label_text.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.loot_count_label.grid(row=5, column=1,padx=10, pady=2, sticky="w")
        self.loot_count_label_text.grid(row=5, column=0,padx=10, pady=2, sticky="w")
        self.loot_var = tk.IntVar(self, 0)

    def start(self):
        if utilities.get_osrs_coordinates() == 0:
            self.update_textbox("Can not find RuneScape window")
            return

        self.pause_button.configure(state='normal')
        self.stop_button.configure(state='normal')
        self.start_button.configure(state='disabled')
        self.is_running = True
        self.start_time = dt.now()

        self.main_button_switch(True)
        if self.script['bot_type'] == 'local':
            bot = combat_bot.CombatBot(self.update_textbox, self.script, self.stop, lambda: self.is_running, lambda: self.is_paused, self.loot_var, mouse_settings=self.mouse_settings)
            self.run = threading.Thread(target=bot.run)
        else:
            bot = gathering_bot.GatheringBot(logs=self.update_textbox, script=self.script, running=lambda: self.is_running, stop=self.stop, paused=lambda: self.is_paused, loot=self.loot_var, mouse_settings=self.mouse_settings)
            self.run = threading.Thread(target=bot.run)

        self.run.start()
        self.clock = threading.Thread(target=self.update_labels, args=(lambda: self.is_running, ))
        self.clock.start()

    def pause(self):
        self.pause_button.configure(text='continue')
        self.update_textbox("Pausing the bot")

    def stop(self):
        if not self.is_running:
            return

        self.update_textbox("{0}Total loot count is {1}\nRun time {2}".format(self.log_box.get('1.0', 'end-1c'), self.loot_var.get(), self.run_time_label.cget('text')))

        if self.save_log.get() == 1:
            date = dt.now()
            file_worker.save_logs(self.log_box.get('1.0', 'end-1c'), self.script["name"], "{0}-{1}-{2}".format(date.day, date.hour, date.minute))

        self.is_running = False
        self.main_button_switch(False)
        self.start_button.configure(state='normal')
        self.pause_button.configure(state='disabled')
        self.start_button.configure(state='disabled')

    def update_textbox(self, text):
        t = time.localtime(time.time())
        local_time = "{0}:{1}:{2} ".format(t.tm_hour, t.tm_min, t.tm_sec)
        self.log_box.configure(state='normal')
        self.log_box.insert(tk.END, local_time+text + "\n")
        self.log_box.configure(state='disabled')
        self.log_box.see('end')

    def update_labels(self, run):
        while run():
            t = dt.now() - self.start_time
            self.run_time_label.configure(text=str(t).split(".")[0])
            self.loot_count_label.configure(text=self.loot_var.get())

    def check_script_state(self):
        pass



