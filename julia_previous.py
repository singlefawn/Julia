# save of latest update

import json
import tkinter as tk
import os
import time
import math
import random
from tkinter import Toplevel
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

        custom_font_path = "admin/assets/century-gothic/CenturyGothic.ttf"
        self.entry_font = (custom_font_path, 14)

        self.text_box = tk.Text(self.text_frame, wrap=tk.WORD, font=self.entry_font, width=50, height=6,
                                bg="black", fg="white", insertbackground="white", borderwidth=0,
                                highlightthickness=0)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Custom scrollbar
        self.scrollbar = tk.Canvas(self.text_frame, bg="black", width=63, height=86, highlightthickness=0)
        scroll_orb_image = Image.open("admin/assets/scroll_orb.png")
        scroll_orb_image = scroll_orb_image.resize((33, 43))
        self.scroll_orb_image = ImageTk.PhotoImage(scroll_orb_image)
        self.slider = self.scrollbar.create_image(31, 43, image=self.scroll_orb_image)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.bind("<B1-Motion>", self.on_scroll)
        self.text_box.bind("<MouseWheel>", self.on_mouse_wheel)

        send_button_image = Image.open("admin/assets/send.png")
        send_button_image = send_button_image.resize((240, 86))
        self.send_button_image = ImageTk.PhotoImage(send_button_image)

        self.submit_button = tk.Label(self.root, image=self.send_button_image, borderwidth=0)
        self.submit_button.pack(pady=10)
        self.submit_button.bind('<Button-1>', lambda event: self.julia_box())

        self.text_box.bind('<Return>', lambda event: self.julia_box())

        # Floating div variables
        self.floating_div = None
        self.gen_counter = 0
        self.show_floating_div = False

        # Bind mouse click event to show/hide floating div
        self.root.bind("<Button-1>", self.show_gen_counter)  # Change this line
       # self.update_gen_counter()

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
        photo_dir = "theta"
        photo_filenames = [f for f in os.listdir(photo_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        random.shuffle(photo_filenames)
        photo = Image.open(os.path.join(photo_dir, photo_filenames[0]))
        width, height = photo.size
        aspect_ratio = width / height
        target_aspect_ratio = 800 / 500
        if aspect_ratio > target_aspect_ratio:
            new_width = 1100
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 500
            new_width = int(new_height * aspect_ratio)
        photo = photo.resize((new_width, new_height))
        self.photo = ImageTk.PhotoImage(photo)
        if hasattr(self, 'photo_label'):
            self.photo_label.config(image=self.photo)  # Update the existing label
        else:
            self.photo_label = tk.Label(self.root, image=self.photo, highlightthickness=0, borderwidth=0)
            self.photo_label.pack(pady=(0, 15))

    def load_new_random_photo(self):
        self.load_random_photo()

    def load_logo(self):
        logo = Image.open("logo.png")
        width, height = logo.size
        aspect_ratio = width / height
        target_width = 100
        target_height = int(target_width / aspect_ratio)
        logo = logo.resize((target_width, target_height))
        self.logo = ImageTk.PhotoImage(logo)
        self.logo_label = tk.Label(self.root, image=self.logo, bg="black")
        self.logo_label.place(x=10, y=10)

    def julia_box(self):
        input_message = self.text_box.get("1.0", tk.END).strip()
        self.create_memory_directory()
        current_ts = int(time.time())
        gen = self.ts_to_gen(current_ts)
        admin = "admin"
        message = (gen, admin, input_message)
        json_file = os.path.join("memory", f"{gen}_Julia.json")
        with open(json_file, 'w') as f:
            json.dump(message, f)
        self.text_box.delete("1.0", tk.END)
        self.text_box.focus_set()
        self.load_new_random_photo()

    def toggle_floating_div(self, event):
        if self.floating_div:
            self.floating_div.destroy()
            self.floating_div = None
        else:
            self.show_floating_div()

    def show_floating_div(self):
        self.floating_div = Toplevel(self.root)
        self.floating_div.overrideredirect(True)
        self.floating_div.attributes('-alpha', 0.8)
        x = random.randint(100, 1200)
        y = random.randint(100, 700)
        self.floating_div.geometry(f"+{x}+{y}")
        self.gen_counter += 1
        gen_label = tk.Label(self.floating_div, text=f"Gen: {self.gen_counter:.2f}", font=("Century Gothic", 9))
        gen_label.pack()
        self.floating_div.after(100, self.show_floating_div)

    def show_gen_counter(self, event):
        x, y = event.x, event.y
        current_ts = int(time.time())
        live_gen = self.ts_to_gen(current_ts)

        if self.floating_div:
            self.floating_div.destroy()
            self.floating_div = None
        else:
            self.floating_div = Toplevel(self.root)
            self.floating_div.overrideredirect(True)
            self.floating_div.attributes('-alpha', 0.8)
            self.floating_div.geometry(f"+{x}+{y}")

            gen_label = tk.Label(self.floating_div, text=f"Live Gen: {live_gen:.6f}", font=("Century Gothic", 9))
            gen_label.pack()

            self.update_live_gen_counter(live_gen)  # Call this method to start updating

    def update_live_gen_counter(self, live_gen):
        if self.floating_div:  # Check if the floating window still exists
            current_ts = int(time.time())
            updated_live_gen = self.ts_to_gen(current_ts)
            gen_label = self.floating_div.winfo_children()[0]
            gen_label.config(text=f" Live Gen • {updated_live_gen:.12f} ")
            self.floating_div.after(1, lambda: self.update_live_gen_counter(updated_live_gen))  # Update every millisecond

    def create_memory_directory(self):
        if not os.path.exists("memory"):
            os.makedirs("memory")

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return gen

julia_box = JuliaBox()
