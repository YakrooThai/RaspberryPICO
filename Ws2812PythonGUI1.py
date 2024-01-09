import tkinter as tk
from tkinter import ttk
import serial

is_port_open = False
serial_port = None

def open_serial():
    global serial_port, is_port_open
    port = com_entry.get()
    try:
        if not is_port_open:
            serial_port = serial.Serial(port, 9600, timeout=1)
            status_label.config(text=f"Serial port {port} opened")
            is_port_open = True
            open_button.config(text="Close Serial Port")
        else:
            serial_port.close()
            status_label.config(text=f"Serial port {port} closed")
            is_port_open = False
            open_button.config(text="Open Serial Port")
    except serial.SerialException:
        status_label.config(text="Error opening/closing serial port")

def send_color():
    com_port = com_entry.get()
    if serial_port and com_port:
        colors = [color_entries[i].get() if color_entries[i].get() else "000000" for i in range(8)]
        serial_data = ",".join(colors) + "\n"
        serial_port.write(serial_data.encode('utf-8'))
        print(serial_data.encode('utf-8'))
    else:
        status_label.config(text="Error opening serial port")

root = tk.Tk()
root.title("Ws2812 Control By YAKROO108")

notebook = ttk.Notebook(root)
notebook.pack(padx=20, pady=20)

# สร้างแท็บสำหรับช่องใส่ค่าสี
color_tab = tk.Frame(notebook)
notebook.add(color_tab, text='Colors')

color_group = tk.LabelFrame(color_tab, text='Color Inputs')
color_group.pack(padx=20, pady=20)

color_entries = []  
for i in range(8):
    label = tk.Label(color_group, text=f"Color {i+1}:")
    label.grid(row=i, column=0, sticky=tk.W)
    color_entry = tk.Entry(color_group, width=8)
    color_entry.grid(row=i, column=1)
    color_entries.append(color_entry)
    
# สร้างปุ่ม "Send Color" และวางไว้ใต้ช่องใส่ค่าสีแบบแถวสุดท้าย
send_button = tk.Button(color_group, text="Send Color", command=send_color)
send_button.grid(row=8, columnspan=2, pady=10)
# สร้างแท็บสำหรับ Serial Port
serial_tab = tk.Frame(notebook)
notebook.add(serial_tab, text='Serial Port')

serial_group = tk.LabelFrame(serial_tab, text='Serial Port Configuration')
serial_group.pack(padx=20, pady=20)

com_label = tk.Label(serial_group, text="Enter COM port:")
com_label.pack()

com_entry = tk.Entry(serial_group)
com_entry.pack()

status_label = tk.Label(serial_group, text="")
status_label.pack(pady=10)

open_button = tk.Button(serial_group, text="Open Serial Port", command=open_serial)
open_button.pack()



root.mainloop()
