import os
import json
import time
import math
import tkinter as tk
from tkinter import messagebox

# Function to generate unique gen number (user ID) with more digits before the decimal
def ts_to_gen(ts):
    gen = math.pow(1.0002, (ts - 1675084800) / 3300)
    return round(gen, 16)

# Function to create a user account folder with user details
def create_user_account(name, handle):
    timestamp = int(time.time())
    user_gen = ts_to_gen(timestamp)

    user_data = {
        "name": name,
        "handle": handle,
        "registration_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
        "gen_number": user_gen
    }

    folder_name = handle.lower()
    folder_path = os.path.join("accounts", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{user_gen:.16f}_{handle.lower()}.json"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as file:
        json.dump(user_data, file, indent=4)

    return handle

# Function to handle the "Create User" button click
def create_user():
    name = entry_name.get()
    handle = entry_handle.get()

    if name.strip() == "" or handle.strip() == "":
        messagebox.showerror("Error", "Please enter a valid name and handle.")
    else:
        created_handle = create_user_account(name, handle)
        messagebox.showinfo("Success", f"Founder account for {created_handle} was successfully formed!")

# GUI setup
root = tk.Tk()
root.title("User Account Creator")
root.geometry("300x250")  # Set the dimensions to 300x250 pixels

label_name = tk.Label(root, text="Enter Name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

label_handle = tk.Label(root, text="Enter Handle:")
label_handle.pack()

entry_handle = tk.Entry(root)
entry_handle.pack()

btn_create = tk.Button(root, text="Create Founder", command=create_user)
btn_create.pack()

root.mainloop()


#