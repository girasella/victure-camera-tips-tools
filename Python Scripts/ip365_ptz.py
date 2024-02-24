import socket
import sys
import time


Left = bytes(b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

Right = bytes(b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

Up = bytes(b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

Down = bytes(b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

# Define byte sequences for other directions (Right, Up, Down)

robot_commands = {
    "left": Left,
    "right": Right,
    "up": Up,
    "down": Down,
}

def forward_command_to_robot(command_socket, robot_socket):
    try:
        while True:
            data = command_socket.recv(1024)
            if not data:
                break

            command = data.decode().strip().lower()
            if command in robot_commands:
                try:
                    robot_socket.sendall(robot_commands[command])
                    print(f"Forwarded command to robot: {command}")
                except (socket.error, socket.timeout):
                    print("Connection to robot lost. Reconnecting...")
                    robot_socket.connect((robot_host, robot_port))
                    print(f"Reconnected to robot at {robot_host}:{robot_port}")
            else:
                print(f"Invalid command received: {command}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        command_socket.close()

def start_proxy():
    local_host = "127.0.0.1"
    local_port = 45678		#The server listens on port 45678 for commands 'left','right','up','down'
    robot_host = "192.168.1.10" #Victure Camera IP Address
    robot_port = 23456

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as command_socket:
        command_socket.bind((local_host, local_port))
        command_socket.listen(1)  # Allow only one connection at a time
        print(f"Proxy listening on {local_host}:{local_port}")

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as robot_socket:
                try:
                    robot_socket.connect((robot_host, robot_port))
                    print(f"Connected to camera at {robot_host}:{robot_port}")

                    client_socket, addr = command_socket.accept()
                    print(f"Accepted connection from {addr}")

                    forward_command_to_robot(client_socket, robot_socket)
                    print(f"Connection with {addr} closed")

                except (socket.error, socket.timeout):
                    print("Error connecting to the camera. Retrying in 5 seconds...")
                    time.sleep(5)

                except KeyboardInterrupt:
                    print("Proxy shutting down.")
                    break

if __name__ == "__main__":
    start_proxy()