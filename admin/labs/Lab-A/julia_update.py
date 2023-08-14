# Julia is more than just a journaling application; it's a personalized assistant designed to be an integral part of the Spider Deer Library system. Set within the innovative and expansive environment of the orbital habitat orbiting planet Anera, Julia serves as a companion, archivist, and helper.
# This module only enables inputs

import json
import tkinter as tk
import os
import time
import math
import random
from PIL import Image, ImageTk


class JuliaBox:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Julia AI")
        self.root.geometry("1600x900")
        self.root.configure(bg="black")

        self.load_random_photo()

        self.text_frame = tk.Frame(self.root, bg="black")
        self.text_frame.pack(pady=(15, 10))

        custom_font_path = "../../assets/century-gothic/CenturyGothic.ttf"  # Relative path to your custom font
        self.entry_font = (custom_font_path, 14)  # Custom font and size

        self.text_box = tk.Text(self.text_frame, wrap=tk.WORD, font=self.entry_font, width=50, height=6,
                                bg="black", fg="white", insertbackground="white", borderwidth=0,
                                highlightthickness=0)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Custom scrollbar
        self.scrollbar = tk.Canvas(self.text_frame, bg="black", width=63, height=86, highlightthickness=0)
        scroll_orb_image = Image.open("../../assets/scroll_orb.png")
        scroll_orb_image = scroll_orb_image.resize((33, 43))
        self.scroll_orb_image = ImageTk.PhotoImage(scroll_orb_image)
        self.slider = self.scrollbar.create_image(31, 43, image=self.scroll_orb_image)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.bind("<B1-Motion>", self.on_scroll)
        self.text_box.bind("<MouseWheel>", self.on_mouse_wheel)

        send_button_image = Image.open("../../assets/send.png")
        send_button_image = send_button_image.resize((240, 86))
        self.send_button_image = ImageTk.PhotoImage(send_button_image)

        self.submit_button = tk.Label(self.root, image=self.send_button_image, borderwidth=0)
        self.submit_button.pack(pady=10)
        self.submit_button.bind('<Button-1>', lambda event: self.julia_box())

        self.text_box.bind('<Return>', lambda event: self.julia_box())

        self.load_logo()

        self.root.mainloop()

    def on_scroll(self, event):
        y = event.y - 43
        self.scrollbar.coords(self.slider, 31, y + 43)
        y_fraction = int(self.text_box.index(tk.END).split(".")[0])
        self.text_box.yview_scroll(int(-1 * (y / self.text_box.winfo_height() * y_fraction)), 'units')

    def on_mouse_wheel(self, event):
        self.text_box.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        y_fraction = float(self.text_box.index(tk.INSERT).split(".")[0]) / float(self.text_box.index(tk.END).split(".")[0])
        y = y_fraction * (self.text_box.winfo_height() - 86) + 43
        self.scrollbar.coords(self.slider, 31, y)

    def load_random_photo(self):
        photo_dir = "../../../theta"  # Directory containing the photos
        photo_filenames = os.listdir(photo_dir)  # List all files in the directory
        photo_filenames = [f for f in photo_filenames if f.endswith(".JPG")]  # Filter for JPG files
        random.shuffle(photo_filenames)  # Shuffle the list to select a random photo
        self.photo = Image.open(
            os.path.join(photo_dir, photo_filenames[0]))  # Load the first photo from the shuffled list
        width, height = self.photo.size  # Get the original size of the image
        aspect_ratio = width / height  # Calculate the aspect ratio
        target_aspect_ratio = 800 / 500  # Set the target aspect ratio
        if aspect_ratio > target_aspect_ratio:
            new_width = 1100
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 500
            new_width = int(new_height * aspect_ratio)
        self.photo = self.photo.resize(
            (new_width, new_height))  # Resize the image to fit the window while preserving aspect ratio
        self.photo = ImageTk.PhotoImage(self.photo)
        self.photo_label = tk.Label(self.root, image=self.photo, highlightthickness=0, borderwidth=0)
        self.photo_label.pack(pady=(0, 15))

    def load_new_random_photo(self):
        self.photo_label.pack_forget()  # Remove the current photo label from the window
        self.text_frame.pack_forget()  # Remove the text frame from the window
        self.submit_button.pack_forget()  # Remove the submit button from the window
        self.load_random_photo()  # Load and display a new random photo
        self.photo_label.pack(pady=(0, 15))  # Repack the photo label
        self.text_frame.pack(pady=(15, 10))  # Repack the text frame
        self.submit_button.pack(pady=10)  # Repack the submit button

    def load_logo(self):
        # Function to load and display the logo image at the top left corner
        logo = Image.open("logo.png")  # Load the logo image
        width, height = logo.size  # Get the original size of the logo
        aspect_ratio = width / height  # Calculate the aspect ratio
        target_width = 100  # Set the target width for the logo
        target_height = int(target_width / aspect_ratio)  # Calculate the target height based on the aspect ratio
        logo = logo.resize(
            (target_width, target_height))  # Resize the logo to target size while preserving aspect ratio
        self.logo = ImageTk.PhotoImage(logo)  # Convert the logo to PhotoImage object
        self.logo_label = tk.Label(self.root, image=self.logo, bg="black")  # Create a label for the logo
        self.logo_label.place(x=10, y=10)  # Place the logo at the top left corner

    def julia_box(self):
        # Function to handle user input and store as JSON

        # Get input from the text box
        input_message = self.text_box.get("1.0", tk.END).strip()

        # Create memory directory if not exists
        self.create_memory_directory()

        # Generate a timestamp as the gen number
        current_ts = int(time.time())
        gen = self.ts_to_gen(current_ts)

        # Assuming the input is from an admin
        admin = "admin"

        # Create a tuple message with the generated number, admin, and input message
        message = (gen, admin, input_message)

        # Create a JSON file path with the generated number
        json_file = os.path.join("../../../memory", f"{gen}_Julia.json")

        # Write the message tuple to the JSON file
        with open(json_file, 'w') as f:
            json.dump(message, f)

        # Clear the text box
        self.text_box.delete("1.0", tk.END)

        # Set focus back to the text box
        self.text_box.focus_set()

        self.load_new_random_photo()  # Load and display a new random photo

    def create_memory_directory(self):
        # Function to create a memory directory if not exists
        if not os.path.exists("../../../memory"):
            os.makedirs("../../../memory")

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return gen


# Create an instance of JuliaBox and run the tkinter event loop
julia_box = JuliaBox()
