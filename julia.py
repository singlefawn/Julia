# julia-ai.py

import json
import tkinter.messagebox as MessageBox
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

        self.entry_font = ("Century Gothic", 12)
        self.input_box = tk.Entry(self.root, font=self.entry_font)
        self.input_box.pack(pady=10)
        self.input_box.config(width=50)

        # Load the custom PNG image for the send button from the specified path
        send_button_image = Image.open("admin/assets/send.png")
        send_button_image = send_button_image.resize((240, 86))
        self.send_button_image = ImageTk.PhotoImage(send_button_image)

        # Create the submit button using the custom image with 0 px border
        self.submit_button = tk.Label(self.root, image=self.send_button_image, borderwidth=0)
        self.submit_button.pack(pady=10)
        self.submit_button.bind('<Button-1>', lambda event: self.julia_box())

        self.input_box.bind('<Return>', lambda event: self.julia_box())

        self.load_logo()

        self.root.mainloop()

    def load_random_photo(self):
        # Function to load and display a random photo from the "foundation" directory
        photo_dir = "theta"  # Directory containing the photos
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
        self.photo_label.pack()

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


    def load_new_random_photo(self):
        # Function to load and display a new random photo
        self.photo_label.pack_forget() # Remove the current photo label from the window
        self.load_random_photo() # Load and display a new random photo

    def julia_box(self):
        # Function to handle user input and store as JSON

        # Get input from the input box
        input_message = self.input_box.get()

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
        json_file = os.path.join("memory", f"{gen}_Julia.json")

        # Write the message tuple to the JSON file
        with open(json_file, 'w') as f:
            json.dump(message, f)

        # Clear the input box
        self.input_box.delete(0, tk.END)

        # Set focus back to input box
        self.input_box.focus_set()

        self.load_new_random_photo() # Load and display a new random photo

    def create_memory_directory(self):
        # Function to create a memory directory if not exists
        if not os.path.exists("memory"):
            os.makedirs("memory")

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return gen


# Create an instance of JuliaBox and run the tkinter event loop
julia_box = JuliaBox()
