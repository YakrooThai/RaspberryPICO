import tkinter as tk
from tkinter import ttk
import serial
import threading
import time

is_port_open = False
serial_port = None
thread_running = False

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
        colors = [color_entries0[i].get() if color_entries0[i].get() else "000000" for i in range(8)]
        serial_data = ",".join(colors) + "\n"
        serial_port.write(serial_data.encode('utf-8'))
        print(serial_data.encode('utf-8'))
    else:
        status_label.config(text="Error opening serial port")
        
def send_color_step(step):
    if serial_port:
        colors = [color_entries[step][i].get() if color_entries[step][i].get() else "000000" for i in range(8)]
        serial_data = ",".join(colors) + "\n"
        serial_port.write(serial_data.encode('utf-8'))
        print(serial_data.encode('utf-8'))
    else:
        status_label.config(text="Error opening serial port")

def start_stop_thread():
    global thread_running
    if not thread_running:
        thread_running = True
        thread = threading.Thread(target=send_color_continuously)
        thread.start()
        start_stop_button.config(text="Stop Sending")
    else:
        thread_running = False
        start_stop_button.config(text="Start Sending")

def send_color_continuously():
    while thread_running:
        for step in range(8):
            send_color_step(step)
            time.sleep(.6)

root = tk.Tk()
root.title("Ws2812 Control By YAKROO108")

notebook = ttk.Notebook(root)
notebook.pack(padx=20, pady=20)

color_tab = tk.Frame(notebook)
notebook.add(color_tab, text='Colors')

color_group = tk.LabelFrame(color_tab, text='Color Inputs')
color_group.pack(padx=20, pady=20)

color_entries = []  
color_entries0 = []  
for i in range(8):
    label = tk.Label(color_group, text=f"Color {i+1}:")
    label.grid(row=i, column=0, sticky=tk.W)
    color_entry = tk.Entry(color_group, width=8)
    color_entry.grid(row=i, column=1)
    color_entries0.append(color_entry)
    
send_button = tk.Button(color_group, text="Send Color", command=send_color)
send_button.grid(row=8, columnspan=2, pady=10)

color_moving_tab = tk.Frame(notebook)
notebook.add(color_moving_tab, text='Colors Moving')

for step in range(8):  
    color_group = tk.LabelFrame(color_moving_tab, text=f'Color Step{step+1}')
    color_group.pack(padx=20, pady=20, side=tk.LEFT)
    
    color_entries_step = []  
    for i in range(8):
        label = tk.Label(color_group, text=f"Color {i+1}:")
        label.grid(row=i, column=0, sticky=tk.W)
        color_entry = tk.Entry(color_group, width=8)
        color_entry.grid(row=i, column=1)
        color_entries_step.append(color_entry)
    
    color_entries.append(color_entries_step)

start_stop_button = tk.Button(color_moving_tab, text="Start Sending", command=start_stop_thread)
start_stop_button.pack(pady=10)

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
