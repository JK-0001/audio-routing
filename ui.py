# GUI using tkinter

import tkinter as tk
from tkinter import ttk
from app import list_sink_inputs, list_sinks, move_sink_input_to_sink
from bluetooth_manager import BluetoothManager

def update_lists():
    sink_inputs = list_sink_inputs()
    sinks = list_sinks()
    bt_devices = bt_manager.scan_devices()

    sink_input_menu["values"] = list(sink_inputs.keys())
    sink_menu["values"] = list(sinks.keys())
    bt_device_menu["values"] = [f"{d[1]} ({d[0]})" for d in bt_devices]

def move_audio():
    sink_input_id = sink_input_var.get()
    sink_id = sink_var.get()
    move_sink_input_to_sink(sink_input_id, sink_id)

root = tk.Tk()
root.title("Audio Router")

sink_input_var = tk.StringVar()
sink_var = tk.StringVar()

ttk.Label(root, text="Select Sink Input:").pack()
sink_input_menu = ttk.Combobox(root, textvariable=sink_input_var)
sink_input_menu.pack()

ttk.Label(root, text="Select Sink:").pack()
sink_menu = ttk.Combobox(root, textvariable=sink_var)
sink_menu.pack()

ttk.Label(root, text="Select Bluetooth Device:").pack()
bt_device_menu = ttk.Combobox(root)
bt_device_menu.pack()

ttk.Button(root, text="Update Lists", command=update_lists).pack()
ttk.Button(root, text="Move Audio", command=move_audio).pack()

bt_manager = BluetoothManager()

root.mainloop()
