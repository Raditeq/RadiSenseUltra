__author__ = "Raditeq"
__copyright__ = "Copyright (C) 2025 Raditeq"
__license__ = "MIT"

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from driver import DeviceConnector

MAX_TIME_USER_INSERT = 1000

# Function to display the graphs 
def display_graphs(NumberOfElements):
    # Generate sample data with 10,000 points
    x = np.linspace(0, NumberOfElements, NumberOfElements)  # 10,000 evenly spaced values between 0 and 10

    device = DeviceConnector("192.168.1.201")  # Port is default (27531)
    device.connect()
    response = device.PerformMeasurement(NumberOfElements)
    device.disconnect()
    yXField, yYField, yZField, yETotField = zip(*response)

    # Create a figure and 4 subplots
    fig, axs = plt.subplots()  # 2x2 grid of subplots

    # First graph: Sine wave
    axs.plot(x, yXField, label='X',  color='blue')
    axs.plot(x, yYField, label='Y', color='red')
    axs.plot(x, yZField, label='Z', color='green')
    axs.plot(x, yETotField, label='ETot', color='purple')
    axs.set_title( f"The number of samples is {NumberOfElements}, in {device.elapsed_time:.3f} seconds measured")
    axs.set_xlabel("samples")
    axs.set_ylabel("V/m")
    axs.legend()
    
    # Adjust layout for better spacing
    plt.tight_layout()

    # Display the graphs
    plt.show()

# Function to handle Start button press
def on_start():  
    try:
        # Get the value from the entry field
        user_value = int(entry.get())

        # Validate the input value
        if 1 <= user_value <= MAX_TIME_USER_INSERT:
            display_graphs(user_value * 1000)  # Call the function with the user's value
        else:
            messagebox.showerror(f"Invalid Input", "Please enter a value between 1 and {MAX_TIME_USER_INSERT}.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer.")


# Main function to start the application
def main():
    # Create the Tkinter GUI
    root = tk.Tk()
    root.title("Timed measurement RadiSense 3018U")

    # Set the size of the window
    root.geometry("400x250")

    # Add a label to explain the input purpose
    info_label = tk.Label(root, text=f"Enter the number of seconds for sampling (1-{MAX_TIME_USER_INSERT}):", font=("Arial", 12))
    info_label.pack(pady=10)  # Add padding for better placement

    # Add an input field
    global entry  # Declare entry as global so it can be accessed in on_start
    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=10)  # Add padding for better placement

    # Add a Start Button
    start_button = tk.Button(root, text="Start measurement", command=on_start, font=("Arial", 14), bg="green", fg="white")
    start_button.pack(pady=20)  # Add padding for better placement

    # Run the GUI event loop
    root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    main()
