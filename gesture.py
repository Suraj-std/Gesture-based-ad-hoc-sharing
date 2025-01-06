import cv2
import mediapipe as mp
import numpy as np
import socket
import os
from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser
import threading
import sys
import time
import signal
import subprocess
import platform

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Gesture thresholds
PINCH_THRESHOLD = 30
HAND_OPEN_THRESHOLD = 70

# File paths
image_path = r"c:\Users\mvsur\Downloads\Living-Room-Essentials-1_original_right_half.jpg"
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
action_state = "None"  # "Server", "Client", or "None"
gesture_detected = False  # Flag to confirm gesture detection
program_running = True  # Flag to control the program flow
cap = None  # Global camera variable


# Server Setup
def get_local_ip():
    """Get the local IP address."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def register_service():
    """Register the server for discovery."""
    try:
        zeroconf = Zeroconf()
        local_ip = get_local_ip()

        service_info = ServiceInfo(
            "_example._tcp.local.",
            "MyServer._example._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=12345,
        )

        zeroconf.register_service(service_info)
        print(f"Service registered with IP: {local_ip}")
        return zeroconf
    except Exception as e:
        print(f"Error registering service: {e}")
        return None


def start_server(image_path):
    """Start the server to send an image."""
    zeroconf = register_service()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((get_local_ip(), 12345))
    server_socket.listen(1)
    print("Server is ready and waiting for a connection...")

    try:
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}. Sending image...")
        filename = os.path.basename(image_path)
        conn.send(f"{filename}\n".encode())
        with open(image_path, "rb") as file:
            while chunk := file.read(1024):
                conn.send(chunk)
        print("Image sent successfully.")
    except Exception as e:
        print(f"Error during server operation: {e}")
    finally:
        if conn:
            conn.close()
        if server_socket:
            server_socket.close()
        if zeroconf:
            zeroconf.unregister_all_services()
            zeroconf.close()


# Client Setup
class MyListener:
    def __init__(self):
        self.server_ip = None

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            # Convert bytes to string for inet_aton
            self.server_ip = socket.inet_ntoa(info.addresses[0])
            print(f"Discovered server IP: {self.server_ip}")


def discover_server():
    """Discover the server."""
    try:
        zeroconf = Zeroconf()
        listener = MyListener()
        ServiceBrowser(zeroconf, "_example._tcp.local.", listener)

        print("Searching for server...")
        start_time = time.time()
        while listener.server_ip is None and time.time() - start_time < 10:
            pass

        zeroconf.close()
        return listener.server_ip
    except Exception as e:
        print(f"Error discovering server: {e}")
        return None


def receive_image(server_ip):
    """Receive an image from the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, 12345))
        print(f"Connected to server at {server_ip}. Receiving image...")

        file_info = b""
        while b"\n" not in file_info:
            file_info += client_socket.recv(1)
        filename = file_info.decode().strip()
        save_path = os.path.join(download_folder, filename)

        with open(save_path, "wb") as file:
            while chunk := client_socket.recv(1024):
                file.write(chunk)

        print(f"Image saved to {save_path}.")
        open_image_in_fullscreen(save_path)
    except Exception as e:
        print(f"Error during client operation: {e}")
    finally:
        client_socket.close()


def open_image_in_fullscreen(image_path):
    """Open the image in the default viewer in full screen."""
    try:
        print(f"Opening image in full screen: {image_path}")
        if platform.system() == "Windows":
            # Open in Photos app and simulate full screen using the F11 key
            subprocess.Popen(["explorer", image_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", image_path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", image_path])
    except Exception as e:
        print(f"Error opening image: {e}")


# Cleanup Function
def cleanup():
    """Clean up resources and exit."""
    global cap, program_running
    program_running = False
    if cap:
        cap.release()
        print("Camera released.")
    cv2.destroyAllWindows()
    print("OpenCV windows closed.")
    sys.exit(0)


# Gesture Detection
def detect_gesture():
    """Detect gestures and decide roles."""
    global action_state, gesture_detected, program_running, cap
    cap = cv2.VideoCapture(0)

    while program_running:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                thumb_tip = np.array([int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)])
                index_tip = np.array([int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)])
                pinch_distance = np.linalg.norm(thumb_tip - index_tip)

                if pinch_distance < PINCH_THRESHOLD and not gesture_detected:
                    action_state = "Server"
                    gesture_detected = True
                elif pinch_distance > HAND_OPEN_THRESHOLD and not gesture_detected:
                    action_state = "Client"
                    gesture_detected = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            program_running = False
            break

    cap.release()


# Signal Handler for Clean Exit
def signal_handler(sig, frame):
    """Handle termination signals."""
    print("\nTermination signal received. Cleaning up...")
    cleanup()


# Main Function
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signal

    gesture_thread = threading.Thread(target=detect_gesture, daemon=True)
    gesture_thread.start()

    try:
        while program_running:
            if action_state == "Server" and gesture_detected:
                print("Acting as Server...")
                start_server(image_path)
                cleanup()

            elif action_state == "Client" and gesture_detected:
                print("Acting as Client...")
                server_ip = discover_server()
                if server_ip:
                    receive_image(server_ip)
                cleanup()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        cleanup()
