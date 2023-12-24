import tkinter as tk
import serial

def open_serial():
    global serial_port
    port = com_entry.get()
    try:
        serial_port = serial.Serial(port, 9600, timeout=1)
        status_label.config(text=f"Serial port {port} opened")
    except serial.SerialException:
        status_label.config(text="Error opening serial port")
        

def send_angle():
    angle = int(scale.get())
    serial_port.write(f"{angle}\n".encode())
    print(f"Sent Servo  Angle: {angle}")

serial_port = None

root = tk.Tk()
root.title("Servo Control By YAKROO108")

com_label = tk.Label(root, text="Enter COM port:")
com_label.pack()

com_entry = tk.Entry(root)
com_entry.pack()

open_button = tk.Button(root, text="Open Serial Port", command=open_serial)
open_button.pack()

label = tk.Label(root, text="Enter servo angle (0-180):")
label.pack()

scale = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL)
scale.pack()

send_button = tk.Button(root, text="Send Angle", command=send_angle)
send_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
