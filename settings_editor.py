import tkinter as tk
from setup_julia import Setup  # Import the Setup class from the setup module

class SettingsEditor:
    def __init__(self, setup_instance):
        self.setup = setup_instance  # Pass the instance of the Setup class

        self.root = tk.Tk()
        self.root.title("Settings Editor")

        self.live_gen_var = tk.BooleanVar(value=self.setup.is_live_gen_enabled())
        self.live_gen_checkbox = tk.Checkbutton(self.root, text="Show Live Gen", variable=self.live_gen_var)
        self.live_gen_checkbox.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_settings)
        self.save_button.pack()

        self.root.mainloop()

    def save_settings(self):
        self.setup.set_live_gen_enabled(self.live_gen_var.get())
        self.root.destroy()

# Create an instance of the Setup class
setup_instance = Setup()

# Create an instance of the SettingsEditor class and pass the setup_instance
settings_editor = SettingsEditor(setup_instance)
