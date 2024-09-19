# # app.py
# from bluetooth_manager import BluetoothManager
# from audio_router import AudioRouter

# def main():
#     bt_manager = BluetoothManager()
#     audio_router = AudioRouter()

#     print("1. Scan for Bluetooth Devices")
#     print("2. List Connected Devices")
#     print("3. List Audio Sinks (Bluetooth Devices)")
#     print("4. List Audio Applications")
#     print("5. Route Application Audio to Device")

#     choice = input("Enter your choice: ")

#     if choice == '1':
#         bt_manager.list_devices()
#     elif choice == '2':
#         bt_manager.list_devices()
#     elif choice == '3':
#         audio_router.list_sinks()
#     elif choice == '4':
#         audio_router.list_applications()
#     elif choice == '5':
#         stream_id = input("Enter Stream ID: ")
#         sink_name = input("Enter Sink Name: ")
#         audio_router.move_stream_to_device(stream_id, sink_name)
#     else:
#         print("Invalid choice!")

# if __name__ == "__main__":
#     main()


####################################################################################################################################
# Main Script with core functionality

import subprocess
from bluetooth_manager import BluetoothManager

def list_sink_inputs():
    """List all sink inputs (active audio streams)."""
    try:
        result = subprocess.run(['pactl', 'list', 'short', 'sink-inputs'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        sink_inputs = {}
        for line in lines:
            parts = line.split()
            sink_input_id = parts[0]
            sink_id = parts[1]
            app_name = ' '.join(parts[2:])
            sink_inputs[sink_input_id] = app_name
        return sink_inputs
    except Exception as e:
        print(f"Error listing sink inputs: {e}")
        return {}

def list_sinks():
    """List all sinks (audio output devices)."""
    try:
        result = subprocess.run(['pactl', 'list', 'short', 'sinks'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        sinks = {}
        for line in lines:
            parts = line.split()
            sink_id = parts[0]
            sink_name = ' '.join(parts[1:])
            sinks[sink_id] = sink_name
        return sinks
    except Exception as e:
        print(f"Error listing sinks: {e}")
        return {}

def move_sink_input_to_sink(sink_input_id, sink_id):
    """Move an audio stream to a specific sink."""
    try:
        subprocess.run(['pactl', 'move-sink-input', sink_input_id, sink_id], check=True)
        print(f"Moved sink input {sink_input_id} to sink {sink_id}")
    except Exception as e:
        print(f"Error moving sink input: {e}")

def main():
    # Initialize BluetoothManager
    bt_manager = BluetoothManager()

    print("Listing active audio streams...")
    sink_inputs = list_sink_inputs()
    for id, name in sink_inputs.items():
        print(f"ID: {id}, Application: {name}")

    print("\nListing audio output devices (sinks)...")
    sinks = list_sinks()
    for id, name in sinks.items():
        print(f"ID: {id}, Sink: {name}")

    print("\nListing Bluetooth devices...")
    bt_manager.list_devices()

    sink_input_id = input("\nEnter the sink input ID to move: ")
    sink_id = input("Enter the sink ID to move it to: ")
    
    move_sink_input_to_sink(sink_input_id, sink_id)

if __name__ == "__main__":
    main()
