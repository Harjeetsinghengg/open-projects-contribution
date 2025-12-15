import cv2
import streamlit as st
import datetime
import os

st.title("Phone Camera Recorder")

# --- User Inputs ---
ip_camera_url = st.text_input(
    "Enter your IP Webcam video URL", 
    value="http://192.168.1.100:8080/video"  # Replace with your phone's IP
)
record_button = st.button("Start Recording")
stop_button = st.button("Stop Recording")

# --- Recording Variables ---
if "recording" not in st.session_state:
    st.session_state.recording = False
if "out" not in st.session_state:
    st.session_state.out = None

# Create recordings folder
if not os.path.exists("recordings"):
    os.makedirs("recordings")

# --- Start Recording ---
if record_button:
    st.session_state.recording = True
    # Capture from IP Webcam
    cap = cv2.VideoCapture(ip_camera_url)
    # Create output file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"recordings/recording_{timestamp}.avi"
    # Define codec and output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    ret, frame = cap.read()
    height, width, _ = frame.shape
    st.session_state.out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    st.session_state.cap = cap
    st.success(f"Recording started → {output_file}")

# --- Stop Recording ---
if stop_button and st.session_state.recording:
    st.session_state.recording = False
    st.session_state.cap.release()
    st.session_state.out.release()
    st.success("Recording stopped")

# --- Main Loop ---
if st.session_state.recording:
    cap = st.session_state.cap
    out = st.session_state.out
    ret, frame = cap.read()
    if ret:
        # Show live feed in Streamlit
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Write frame to file
        out.write(frame)
