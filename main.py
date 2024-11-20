import cv2
import tkinter as tk
from tkinter import StringVar, ttk, filedialog
from PIL import Image, ImageTk
import threading
import gc
import time

# Global variables
is_inverted = True
cap = None
current_camera_index = None
stop_event = threading.Event()
cap_lock = threading.Lock()
uploaded_image = None  # To store the uploaded image

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
    with cap_lock:
        if new_camera_index != current_camera_index:
            if cap is not None:
                cap.release()
                time.sleep(0.1)
            cap = cv2.VideoCapture(new_camera_index)
            if cap.isOpened():
                current_camera_index = new_camera_index
            gc.collect()

# Capture and save an image
def capture_and_save():
    def capture():
        with cap_lock:
            if cap is not None:
                ret, frame = cap.read()
                if ret:
                    if is_inverted:
                        frame = cv2.flip(frame, 1)
                    threading.Thread(target=process_and_save_image, args=(frame,)).start()

    threading.Thread(target=capture).start()

def upload_and_save():
    def upload():
        # Open a file dialog to choose a .png file
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])

        if file_path:
            # Load the image using OpenCV
            global uploaded_image
            uploaded_image = cv2.imread(file_path)
            show_popup()

    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    threading.Thread(target=upload).start()

# Process and save the image
def process_and_save_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
    line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    resized_image = cv2.resize(line_drawing_frame, (640, 360))
    cv2.imwrite("line_drawing.png", resized_image)
    print("Image captured and saved as line_drawing.png")
    gc.collect()

# Invert the camera view
def invert_camera():
    global is_inverted
    is_inverted = not is_inverted

# Update the camera feed
def update_camera():
    while not stop_event.is_set():
        if not root.winfo_exists():  # Ensure window exists
            break
        with cap_lock:
            if cap is not None:
                ret, frame = cap.read()
                if ret:
                    if is_inverted:
                        frame = cv2.flip(frame, 1)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
                    line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                    line_drawing_frame = cv2.cvtColor(line_drawing_frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(Image.fromarray(line_drawing_frame))
                    # Check if the window is still open before updating the canvas
                    if root.winfo_exists():
                        canvas.create_image((canvas.winfo_width() - photo.width()) // 2,
                                            (canvas.winfo_height() - photo.height()) // 2,
                                            image=photo, anchor=tk.NW)
                        canvas.image = photo
        time.sleep(0.03)

# Graceful exit when closing the window
def on_closing():
    stop_event.set()  # Signal the camera thread to stop
    if cap is not None:
        cap.release()  # Release the camera
    root.quit()  # Quit the Tkinter event loop
    root.destroy()  # Destroy the Tkinter root window
    gc.collect()  # Run garbage collection to clean up resources


# Show popup for the uploaded image
def show_popup():
    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Edit Image")
    popup.geometry("800x600")

    # Create a canvas to display the uploaded image
    canvas_popup = tk.Canvas(popup, width=640, height=360)
    canvas_popup.pack(pady=10)

    # Display the uploaded image on the canvas
    def update_canvas():
        sensitivity = sensitivity_slider_popup.get()
        gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=sensitivity, threshold2=sensitivity * 3)
        line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        resized_image = cv2.resize(line_drawing_frame, (640, 360))
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(resized_image_rgb))
        canvas_popup.create_image(320, 180, image=photo)
        canvas_popup.image = photo

    # Add sensitivity slider
    ttk.Label(popup, text="Sensitivity").pack(pady=5)
    sensitivity_slider_popup = ttk.Scale(popup, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda event: update_canvas())
    sensitivity_slider_popup.set(30)
    sensitivity_slider_popup.pack(pady=10)

    # Initial canvas update
    update_canvas()

    # Save button to save the image after processing
    def save_image():
        sensitivity = sensitivity_slider_popup.get()
        gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=sensitivity, threshold2=sensitivity * 3)
        line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        resized_image = cv2.resize(line_drawing_frame, (640, 360))
        cv2.imwrite("line_drawing.png", resized_image)
        print("Image saved as line_drawing.png")
        popup.destroy()

    save_button = ttk.Button(popup, text="Save", command=save_image)
    save_button.pack(pady=10)

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
        command=lambda _: threading.Thread(target=change_camera, args=(camera_list[camera_names.index(selected_camera.get())][1],)).start())
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

# Start the camera update thread
threading.Thread(target=update_camera, daemon=True).start()

# Close event handling
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
