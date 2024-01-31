import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

def open_image():
    # Prompt user to select a BMP file
    file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])

    if file_path:
        # Hide "No Picture" label
        no_picture_label.pack_forget()

        tk_image = ImageTk.PhotoImage(Image.open(file_path))

        # Update the image label
        image_label.config(image=tk_image)
        image_label.image = tk_image

        # Display image dimensions
        dimensions_label.config(text=f"Image Dimensions: {tk_image.width()} x {tk_image.height()}")

        # Store the selected file path globally for later use
        global selected_file_path
        selected_file_path = file_path

def open_serial():
    global serial_port
    port = comport_entry.get()
    try:
        serial_port = serial.Serial(port, 9600, timeout=1)
        status_label.config(text=f"Serial port {port} opened")
    except serial.SerialException:
        status_label.config(text="Error opening serial port")

def send_file():
    global selected_file_path

    # Prompt user to enter a file name
    file_name = file_name_entry.get()

    # Prompt user to select a directory for saving the image
    save_directory = filedialog.askdirectory()

    if save_directory and selected_file_path:
        # Open the selected image file
        with Image.open(selected_file_path) as img:
            # Save the image as a BMP file in the selected directory
            output_path = os.path.join(save_directory, f"{file_name}.bmp")
            img.save(output_path, format="BMP")
            status_label.config(text=f"Image saved to {output_path}")
    else:
        status_label.config(text="Error: Invalid file or directory")

# Initialize the selected file path
selected_file_path = None

# Create the main window
main_window = tk.Tk()
main_window.title("RaspberryPICO Photo View")

# Set the window size (width x height)
main_window.geometry("480x320")  # ตัวอย่างขนาดหน้าต่าง 480x320 pixels

# Create a frame for the left side (image display)
left_frame = tk.Frame(main_window)
left_frame.pack(side=tk.LEFT)

# Create a label for "No Picture"
no_picture_label = tk.Label(left_frame, text="No Picture")
no_picture_label.pack()

# Create a Tkinter PhotoImage for initial image label
initial_image = ImageTk.PhotoImage(Image.new("RGB", (1, 1)))  # Create a small blank image
image_label = tk.Label(left_frame, image=initial_image)
image_label.pack()

# Display image dimensions
dimensions_label = tk.Label(left_frame, text="Pixel: N/A")
dimensions_label.pack()

status_label = tk.Label(main_window, text="Select Picture")
status_label.pack()

# Create a button to open an image file
open_image_button = tk.Button(main_window, text="Open Image", command=open_image)
open_image_button.pack(pady=10)

# Create an entry for file name
file_name_entry = tk.Entry(main_window, width=20)
file_name_entry.pack()

# Create a button to send a file
send_file_button = tk.Button(main_window, text="Send File", command=send_file)
send_file_button.pack(pady=10)

# Run the Tkinter event loop for the main window
main_window.mainloop()
