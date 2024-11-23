import cv2
import tkinter as tk
from tkinter import StringVar, ttk, filedialog
from PIL import Image, ImageTk
import threading
import queue
import time

# Global variables
is_inverted = True
cap = None
current_camera_index = None
uploaded_image = None  # To store the uploaded image
frame_queue = queue.Queue(maxsize=1)  # Queue to hold the latest frame

# Detect available cameras
def detect_cameras():
    camera_list = []
    for i in range(10):
        temp_cap = cv2.VideoCapture(i)
        if temp_cap.isOpened():
            camera_list.append((f"Camera {i}", i))
            temp_cap.release()
    return camera_list

# Change the camera
def change_camera(new_camera_index):
    global cap, current_camera_index
    if new_camera_index != current_camera_index:
        if cap is not None:
            cap.release()
            time.sleep(0.1)  # Short delay to avoid potential race condition
        cap = cv2.VideoCapture(new_camera_index)
        if cap.isOpened():
            current_camera_index = new_camera_index

# Capture and save an image
def capture_and_save():
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            if is_inverted:
                frame = cv2.flip(frame, 1)
            process_and_save_image(frame)

def upload_and_save():
    # Open a file dialog to choose a .png file
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])

    if file_path:
        # Load the image using OpenCV
        global uploaded_image
        uploaded_image = cv2.imread(file_path)
        # Run the image processing for the popup in a separate thread
        threading.Thread(target=process_uploaded_image, daemon=True).start()
        show_popup()

# Process and save the image
def process_and_save_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
    line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    resized_image = cv2.resize(line_drawing_frame, (640, 360))
    cv2.imwrite("line_drawing.png", resized_image)
    print("Image captured and saved as line_drawing.png")

# Invert the camera view
def invert_camera():
    global is_inverted
    is_inverted = not is_inverted

# Worker thread to capture frames from the camera
def capture_frame():
    while True:
        if cap is not None and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if is_inverted:
                    frame = cv2.flip(frame, 1)
                if not frame_queue.full():
                    frame_queue.put(frame)
        time.sleep(0.03)  # Capture every 30 ms

# Update the camera feed on the canvas (called from the main thread)
def update_camera():
    if not frame_queue.empty():
        frame = frame_queue.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
        line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        line_drawing_frame_rgb = cv2.cvtColor(line_drawing_frame, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(line_drawing_frame_rgb)
        photo = ImageTk.PhotoImage(pil_image)

        if root.winfo_exists():
            canvas.create_image((canvas.winfo_width() - photo.width()) // 2,
                                (canvas.winfo_height() - photo.height()) // 2,
                                image=photo, anchor=tk.NW)
            canvas.image = photo  # Keep reference to avoid garbage collection

    # Schedule the next camera update (every 30 ms)
    root.after(30, update_camera)

# Graceful exit when closing the window
def on_closing():
    if cap is not None:
        cap.release()  # Release the camera
    root.quit()  # Quit the Tkinter event loop
    root.destroy()  # Destroy the Tkinter root window

# Show popup for the uploaded image
def show_popup():
    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Edit Image")
    popup.geometry("800x600")

    # Create a canvas to display the uploaded image
    canvas_popup = tk.Canvas(popup, width=640, height=360)
    canvas_popup.pack(pady=10)

    # Function to update the canvas in the popup window
    def update_popup_canvas(processed_image):
        pil_image = Image.fromarray(processed_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        canvas_popup.create_image(320, 180, image=photo)
        canvas_popup.image = photo  # Keep reference to avoid garbage collection

    # Add sensitivity slider
    ttk.Label(popup, text="Sensitivity").pack(pady=5)
    sensitivity_slider_popup = ttk.Scale(popup, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda event: update_popup_canvas(process_uploaded_image()))
    sensitivity_slider_popup.set(30)
    sensitivity_slider_popup.pack(pady=10)

    # Initial canvas update (when popup opens)
    processed_image = process_uploaded_image()
    update_popup_canvas(processed_image)

    # Save button to save the image after processing
    def save_image():
        processed_image = process_uploaded_image()
        cv2.imwrite("line_drawing.png", processed_image)
        print("Image saved as line_drawing.png")
        popup.destroy()

    save_button = ttk.Button(popup, text="Save", command=save_image)
    save_button.pack(pady=10)

# Function to process the uploaded image (run in a background thread)
def process_uploaded_image():
    if uploaded_image is not None:
        gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
        line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        resized_image = cv2.resize(line_drawing_frame, (640, 360))
        return resized_image

# GUI setup
root = tk.Tk()
root.title("Camera Feed")

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

# Control frame
control_frame = tk.Frame(root)
control_frame.pack(side='top', pady=10, fill="x")

# Configure grid layout for alignment
control_frame.columnconfigure(1, weight=0)  # Upload button
control_frame.columnconfigure(2, weight=1)  # Center spacer
control_frame.columnconfigure(3, weight=0)  # Camera menu
control_frame.columnconfigure(4, weight=0)  # Take Photo button
control_frame.columnconfigure(5, weight=0)  # Invert button
control_frame.columnconfigure(6, weight=1)  # Right spacer
control_frame.columnconfigure(7, weight=0)  # Sensitivity label
control_frame.columnconfigure(8, weight=0)  # Sensitivity slider

# Upload button (far left)
upload_button = ttk.Button(control_frame, text="Upload Image", command=upload_and_save)
upload_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Camera list dropdown
camera_list = detect_cameras()
selected_camera = StringVar(value="Select camera")
if camera_list:
    camera_names = [name for name, _ in camera_list]
    camera_menu = ttk.OptionMenu(
        control_frame, selected_camera, "Select camera", *camera_names,
        command=lambda _: change_camera(camera_list[camera_names.index(selected_camera.get())][1]))
    camera_menu.grid(row=1, column=3, padx=10, pady=10)

# Center buttons
photo_button = ttk.Button(control_frame, text="Take Photo", command=capture_and_save)
photo_button.grid(row=1, column=4, padx=10, pady=10)

invert_button = ttk.Button(control_frame, text="Invert Camera", command=invert_camera)
invert_button.grid(row=1, column=5, padx=10, pady=10)

# Sensitivity slider and label (far right)
ttk.Label(control_frame, text="Sensitivity").grid(row=0, column=8, padx=5, pady=0, sticky="e")
sensitivity_slider = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL)
sensitivity_slider.set(30)
sensitivity_slider.grid(row=1, column=8, padx=10, pady=10, sticky="e")

# Initialize camera
if camera_list:
    change_camera(camera_list[0][1])

# Start the frame capture thread
capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread.start()

# Start the camera update loop
update_camera()

# Close event handling
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
