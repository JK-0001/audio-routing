import subprocess
import re

def list_sink_inputs():
    """List all sink inputs (active audio streams) with application names."""
    try:
        result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')

        sink_inputs = {}
        current_sink_input_id = None
        current_app_name = None

        for line in lines:
            # Match sink input ID
            sink_input_match = re.search(r"Sink Input #(\d+)", line)
            if sink_input_match:
                current_sink_input_id = sink_input_match.group(1)
            
            # Match application name
            app_name_match = re.search(r"application.name = \"([^\"]+)\"", line)
            if app_name_match and current_sink_input_id:
                current_app_name = app_name_match.group(1)
                sink_inputs[current_sink_input_id] = current_app_name
                current_sink_input_id = None  # Reset for the next sink input

        return sink_inputs
    except Exception as e:
        print(f"Error listing sink inputs: {e}")
        return {}

def list_sinks():
    """List all sinks (audio output devices) with human-readable names."""
    try:
        result = subprocess.run(['pactl', 'list', 'sinks'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')

        sinks = {}
        current_sink_id = None
        current_sink_description = None

        for line in lines:
            # Match sink ID
            sink_match = re.search(r"Sink #(\d+)", line)
            if sink_match:
                current_sink_id = sink_match.group(1)
            
            # Match sink description (usually the device name)
            sink_description_match = re.search(r"Description: (.+)", line)
            if sink_description_match and current_sink_id:
                current_sink_description = sink_description_match.group(1)
                sinks[current_sink_id] = current_sink_description
                current_sink_id = None  # Reset for the next sink

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

    print("Listing active audio streams...")
    sink_inputs = list_sink_inputs()
    if sink_inputs:
        for id, app_name in sink_inputs.items():
            print(f"Sink Input ID: {id}, Application: {app_name}")
    else:
        print("No active audio streams found.")

    print("\nListing audio output devices (sinks)...")
    sinks = list_sinks()
    if sinks:
        for id, name in sinks.items():
            print(f"Sink ID: {id}, Output Device: {name}")
    else:
        print("No audio output devices found.")

    sink_input_id = input("\nEnter the sink input ID to move: ")
    sink_id = input("Enter the sink ID to move it to: ")
    
    move_sink_input_to_sink(sink_input_id, sink_id)

if __name__ == "__main__":
    main()
