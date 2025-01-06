# Gesture-Based File Sharing System

## 🚀 Overview
The **Gesture-Based File Sharing System** utilises computer vision, gesture recognition, and ad-hoc networking to enable seamless file sharing between devices. By detecting hand gestures via a webcam, the system dynamically assigns roles (server or client) and facilitates the secure transfer of files.

## 📜 Features
- **Gesture Recognition**:
  - Pinch Gesture: Assigns the device as a server.
  - Open Hand Gesture: Assigns the device as a client.
- **Platform Compatibility**: Works across Windows, macOS, and Linux.
- **Ad-Hoc Networking**: Uses `zeroconf` for service discovery and socket programming for secure file sharing.
- **Cross-Platform File Viewer**: Automatically opens shared files in full-screen mode.

## 🛠️ Technologies Used
- **Python**: Main programming language.
- **MediaPipe**: For real-time gesture detection and hand tracking.
- **OpenCV**: For video capture and processing.
- **Socket Programming**: Facilitates file transfer between devices.
- **Zeroconf**: Enables device discovery without external configuration.

## 🏗️ Project Structure
```plaintext
├── gesture.py  # Main script for gesture detection and file sharing
```

## ⚙️ How It Works
1. **Gesture Detection**:
   - Detects gestures (pinch or open hand) using MediaPipe and OpenCV.
   - Dynamically assigns the device as either a server or a client.

2. **Server**:
   - Hosts a file for sharing using an ad-hoc network.
   - Uses `zeroconf` for discovery and AES encryption for secure transfer.

3. **Client**:
   - Discovers the server on the network.
   - Downloads and saves the shared file to a specified location.
   - Opens the file in full-screen mode.

## 📂 Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Required libraries (install via `requirements.txt`):
  ```plaintext
  pip install mediapipe
  pip install opencv-python
  pip install zeroconf
  pip install numpy
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gesture-sharing.git
   cd gesture-sharing
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
#### Start the System
   ```bash
   python gesture_sharing.py
   ```
   - Use gestures to assign roles:
     - **Pinch Gesture**: Acts as server.
     - **Open Hand Gesture**: Acts as client.

## 📸 Screenshots
### Server in Action
![Server in Action](https://via.placeholder.com/400x200.png?text=Server+Running)
### Client Receiving File
![Client Receiving File](https://via.placeholder.com/400x200.png?text=Client+Receiving+File)

## 🔒 Security Highlights
- **Ad-Hoc Network**: Peer-to-peer device connection without external configuration.
- **Cross-Platform Compatibility**: Works on all major operating systems.

## 🤝 Contributing
Contributions are welcome! Follow these steps to get started:
1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
- Email: [your.email@example.com](mailto:your.email@example.com)
- GitHub: [yourusername](https://github.com/yourusername)
