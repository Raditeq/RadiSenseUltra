__author__ = "Raditeq"
__copyright__ = "Copyright (C) 2025 Raditeq"
__license__ = "MIT"

import socket
import time
import struct

class DeviceConnector:
    # size = 21 
    #  #<headersize 1 byte><header 2 byte><data x 4 bytes><data y 4 bytes><data z 4 bytes><data ETot 4 bytes>\n
    _BIN_FRAME_SIZE = 21

    def __init__(self, ip, port=27531, timeout=5):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.elapsed_time = 0

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.ip, self.port))

            # Check if the version is greater than or equal to 1.3.0 right after connecting
            if not self._is_version_at_least("1.3.0"):
                print("Warning: Device firmware version is below 1.3.0.")
                self.disconnect()  # Optionally disconnect if version is not sufficient
            else:
                print("Device connected and version is 1.3.0 or above.")

        except socket.error as e:
            print(f"Connection error: {e}")
            self.socket = None

    def PerformMeasurement(self, num_samples): 
        # Set filter 5 so we can use the 
        self.send_command_and_check_ok("FILTER 5")
        # the +1 is in case we are not syncronised with the stream.
        totalofBytes = (num_samples + 1) * self._BIN_FRAME_SIZE
        print(totalofBytes)

        self.send_command_and_check_ok("STARTTIMED 1")

        # Record the start time
        start_time = time.perf_counter()
        #read the data
        dataArray = self.read_exact_bytes(totalofBytes)
        # Record the end time
        end_time = time.perf_counter()
        
        #stop the stream
        self.send_command("STOPTIMED")

        # Calculate and print the elapsed time
        self.elapsed_time = end_time - start_time
        print(f"Function execution time: {self.elapsed_time} seconds")

        frames = self._extract_frames(dataArray)
 
        fieldMeasurements = []
        for frame in frames:
            fieldMeasurements.append(self._extract_floats(frame))

        return fieldMeasurements[:num_samples]

    def _extract_frames(self, byte_array):
        frame_size = self._BIN_FRAME_SIZE
        start_marker = b'#216'  # Frame starts with '#216'
        end_marker = b'\n'  # Frame ends with '\n'        
        frames = []
        index = 0
        
        # Loop through the byte array to extract frames
        while index + frame_size <= len(byte_array):
            frame = byte_array[index:index + frame_size]
            
            # Check if frame starts with '#216' and ends with '\n'
            if frame.startswith(start_marker) and frame.endswith(end_marker):
                frames.append(frame)
            
            # Move to the next frame (21 bytes ahead)
            index += frame_size
        
        return frames

    def _extract_floats(self, byte_array):
        # Define frame size and markers
        header = b'#216'
        footer = b'\n'
        frame_size = 21  # 4 bytes per float * 4 floats + header (3 bytes) + footer (1 byte)
        
        # Check that the byte array has the expected structure
        if byte_array.startswith(header) and byte_array.endswith(footer):
            # Extract the data part (bytes between header and footer)
            data = byte_array[len(header):-len(footer)]  # Exclude header and footer
            
            # Ensure the data is the correct size (16 bytes for 4 floats)
            if len(data) == 16:
                # Unpack the 16 bytes into 4 floats (each 4 bytes)
                #floats = struct.unpack('!4f', data)
                floats = struct.unpack('<4f', data)
                return floats
            else:
                raise ValueError("Data length is incorrect, expected 16 bytes for 4 floats.")
        else:
            raise ValueError("Frame does not have the expected header or footer.")

    def read_exact_bytes(self, num_bytes):
        data = b''  # Initialize an empty byte string
        while len(data) < num_bytes:
            remaining_bytes = num_bytes - len(data)
            chunk = self.socket.recv(remaining_bytes)  # Read the remaining bytes
            if not chunk:
                raise IOError("Socket connection closed before receiving the desired number of bytes.")
            data += chunk  # Append the received chunk to the data
        return data

    def _get_firmware_version(self):
        # Send the IDN query to the device
        response = self.send_command("*IDN?")
        if response:
            print(f"Device response: {response}")
            # Assuming the version is part of the response, e.g., "Raditeq, RadiSense LPS3001A, 1.3.1"
            return response.split(',')[-1].strip()  # Extracting version (assuming version is the last part)
        return None

    def _is_version_at_least(self, version_check):
        current_version = self._get_firmware_version()
        if current_version:
            current_version_parts = current_version.split('.')
            check_version_parts = version_check.split('.')
            
            # Compare the version parts (major, minor, patch)
            for i in range(min(len(current_version_parts), len(check_version_parts))):
                if int(current_version_parts[i]) > int(check_version_parts[i]):
                    return True
                elif int(current_version_parts[i]) < int(check_version_parts[i]):
                    return False
            # If all parts are the same, then the versions are equal
            return True
        return False

    def _recv_line(self):
        """Reads data from the socket until a newline is encountered."""
        response = ''
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break  # Connection is closed
                response += data.decode('utf-8', errors='ignore')
                if '\n' in response:
                    break  # Stop reading when we encounter a newline
            except socket.error as e:
                print(f"Error receiving data: {e}")
                break
        return response.strip()  # Remove any extra newline characters

    def send_command(self, command):
        if not self.socket:
            print("Not connected to the device.")
            return None
        
        # Ensure the command ends with a newline
        if not command.endswith('\n'):
            command += '\n'
        try:
            self.socket.sendall(command.encode('utf-8'))
            return self._recv_line()             
        except socket.error as e:
            print(f"Communication error: {e}")
            return None

    def send_command_and_check_ok(self, command):
        # Sends the command and checks if the response contains "OK"
        response = self.send_command(command)
        if response:
            if "OK" in response:                
                return True
            else:
                print(f"Command failed, response: {response}")
        else:
            print("No response received.")
        return False

    def get_elapsed_time(self):
        """Retrieve the stored elapsed time."""
        return self.elapsed_time

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

if __name__ == "__main__":
    device = DeviceConnector("192.168.32.62")  # Port is default (27531)
    device.connect()
    response = device.PerformMeasurement(1000)
    if response:
        print(response)
    device.disconnect()
