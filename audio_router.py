# audio_router.py
import subprocess

class AudioRouter:
    def list_sinks(self):
        # List all available sinks (audio devices)
        result = subprocess.run(['pactl', 'list', 'short', 'sinks'], stdout=subprocess.PIPE)
        sinks = result.stdout.decode('utf-8')
        print(sinks)

    def list_applications(self):
        # List all active audio streams (applications)
        result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
        inputs = result.stdout.decode('utf-8')
        print(inputs)

    def move_stream_to_device(self, stream_id, sink_name):
        # Move the specified audio stream (stream_id) to the specified sink (sink_name)
        subprocess.run(['pactl', 'move-sink-input', str(stream_id), sink_name])
        print(f"Moved stream {stream_id} to {sink_name}")
