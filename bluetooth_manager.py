# # from gi.repository import GLib
# from pydbus import SystemBus
# import time

# class BluetoothManager:
#     def __init__(self):
#         self.bus = SystemBus()

#         # Get the BlueZ ObjectManager (to list managed objects)
#         self.manager = self.bus.get('org.bluez', '/')
        
#         # Get the adapter interface (hci0 is the typical default adapter)
#         self.adapter = self.bus.get('org.bluez', '/org/bluez/hci0')

#     def scan_devices(self):
#         # Start Bluetooth device discovery
#         try:
#             self.adapter.StartDiscovery()
#             print("Scanning for Bluetooth devices...")
#         except Exception as e:
#             print(f"Error starting discovery: {e}")
#             return []

#         # Sleep for a while to allow discovery to find devices
#         time.sleep(5)

#         # Stop scanning
#         self.adapter.StopDiscovery()

#         # Get all managed objects (Bluetooth devices and other BlueZ objects)
#         devices = self.manager.GetManagedObjects()

#         found_devices = []
#         for path, interfaces in devices.items():
#             if 'org.bluez.Device1' in interfaces:
#                 device_info = interfaces['org.bluez.Device1']
#                 address = device_info.get('Address')
#                 name = device_info.get('Name', 'Unknown')
#                 found_devices.append((address, name))

#         return found_devices

#     def list_devices(self):
#         devices = self.scan_devices()
#         if devices:
#             print("Devices Found:")
#             for idx, device in enumerate(devices):
#                 print(f"{idx}: {device[1]} ({device[0]})")
#         else:
#             print("No devices found.")

#     def connect_device(self, device_address):
#         device_path = f"/org/bluez/hci0/dev_{device_address.replace(':', '_')}"
#         try:
#             device = self.bus.get("org.bluez", device_path)
#             device.Connect()
#             print(f"Connected to {device_address}")
#         except Exception as e:
#             print(f"Failed to connect to {device_address}: {str(e)}")


####################################################################################################################################
# BLuetooth Manager class to manage Bluetooth devices
# This class uses pydbus library to communicate with BlueZ over D-Bus
# It provides methods to scan for devices, list devices, connect to devices, and disconnect from devices

from pydbus import SystemBus
import time

class BluetoothManager:
    def __init__(self):
        self.bus = SystemBus()

        # Get the BlueZ ObjectManager (to list managed objects)
        try:
            self.manager = self.bus.get('org.bluez', '/')
        except Exception as e:
            print(f"Failed to connect to BlueZ ObjectManager: {e}")
            self.manager = None
        
        # Get the adapter interface (hci0 is the typical default adapter)
        try:
            self.adapter = self.bus.get('org.bluez', '/org/bluez/hci0')
        except Exception as e:
            print(f"Failed to connect to Bluetooth adapter: {e}")
            self.adapter = None

    def scan_devices(self):
        if not self.adapter:
            print("Bluetooth adapter not available.")
            return []

        # Start Bluetooth device discovery
        try:
            self.adapter.StartDiscovery()
            print("Scanning for Bluetooth devices...")
        except Exception as e:
            print(f"Error starting discovery: {e}")
            return []

        # Sleep for a while to allow discovery to find devices
        time.sleep(5)

        # Stop scanning
        try:
            self.adapter.StopDiscovery()
        except Exception as e:
            print(f"Error stopping discovery: {e}")

        # Get all managed objects (Bluetooth devices and other BlueZ objects)
        if not self.manager:
            print("BlueZ ObjectManager not available.")
            return []

        devices = self.manager.GetManagedObjects()

        found_devices = []
        for path, interfaces in devices.items():
            if 'org.bluez.Device1' in interfaces:
                device_info = interfaces['org.bluez.Device1']
                address = device_info.get('Address')
                name = device_info.get('Name', 'Unknown')
                found_devices.append((address, name))

        return found_devices

    def list_devices(self):
        devices = self.scan_devices()
        if devices:
            print("Devices Found:")
            for idx, device in enumerate(devices):
                print(f"{idx}: {device[1]} ({device[0]})")
        else:
            print("No devices found.")

    def connect_device(self, device_address):
        device_path = f"/org/bluez/hci0/dev_{device_address.replace(':', '_')}"
        try:
            device = self.bus.get("org.bluez", device_path)
            device.Connect()
            print(f"Connected to {device_address}")
        except Exception as e:
            print(f"Failed to connect to {device_address}: {str(e)}")

if __name__ == "__main__":
    manager = BluetoothManager()
    manager.list_devices()
    # Example usage to connect to a device
    # manager.connect_device("XX:XX:XX:XX:XX:XX")
