Air Canvas – Finger Tracking Virtual Painter

Air Canvas is a computer vision-based virtual painting application that allows users to draw in the air using hand gestures. It leverages real-time hand tracking to transform finger movements into digital strokes on the screen.

🚀 Features
✋ Real-time finger tracking using webcam
🎨 Draw in the air without touching the screen
🌈 Multiple color selection options
🧹 Eraser functionality for corrections
⚡ Smooth and responsive drawing experience
🛠️ Tech Stack
Python
OpenCV
MediaPipe (Hand Tracking)
NumPy
📸 How It Works
Webcam captures live video feed
Hand landmarks are detected using MediaPipe
Index finger movement is tracked
Movements are mapped to drawing on the screen
▶️ How to Run

Clone the repository:

git clone https://github.com/meghana-1006/Hand-gesture-virtual-painter

Navigate to the project folder:

cd Hand-gesture-virtual-painter

Install dependencies:

pip install opencv-python mediapipe numpy

Run the application:

python aircanvas.py
