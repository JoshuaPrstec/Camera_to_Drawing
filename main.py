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

def detect_cameras():
    camera_list = []
    index = 0
    while True:
        temp_cap = cv2.VideoCapture(index)
        if temp_cap.isOpened():
            camera_list.append((f"Camera {index}", index))
            temp_cap.release()
        else:
            temp_cap.release()
            break  # Stop checking further indices if the current one is not available
        index += 1
    return camera_list

# Change the camera
def change_camera(new_camera_index):
    global cap, current_camera_index
    if new_camera_index != current_camera_index:
        if cap is not None:
            cap.release()
            time.sleep(0.1)
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

# Upload and save an image
def upload_and_save():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if file_path:
        global uploaded_image
        uploaded_image = cv2.imread(file_path)
        show_popup()

# Process and save the image
def process_and_save_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sensitivity = int(sensitivity_slider.get())
    edges = cv2.Canny(gray, threshold1=sensitivity, threshold2=sensitivity * 3)
    line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    resized_image = cv2.resize(line_drawing_frame, (640, 360))
    cv2.imwrite("line_drawing.png", resized_image)
    print("Image captured and saved as line_drawing.png")

# Invert the camera view
def invert_camera():
    global is_inverted
    is_inverted = not is_inverted
    print("Camera is inverted")

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
        time.sleep(0.03)

# Update the camera feed on the canvas
def update_camera():
    if not frame_queue.empty():
        frame = frame_queue.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sensitivity = int(sensitivity_slider.get())
        edges = cv2.Canny(gray, threshold1=sensitivity, threshold2=sensitivity * 3)
        line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        line_drawing_frame_rgb = cv2.cvtColor(line_drawing_frame, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(line_drawing_frame_rgb)
        photo = ImageTk.PhotoImage(pil_image)

        if root.winfo_exists():
            canvas.create_image((canvas.winfo_width() - photo.width()) // 2,
                                (canvas.winfo_height() - photo.height()) // 2,
                                image=photo, anchor=tk.NW)
            canvas.image = photo

    root.after(30, update_camera)

def on_closing():
    global cap
    if cap is not None:
        cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Destroy OpenCV windows (if any)
    root.quit()
    root.destroy()

# Show popup for the uploaded image
def show_popup():
    def update_popup_canvas(sensitivity):
        processed_image = process_uploaded_image(sensitivity)
        pil_image = Image.fromarray(processed_image)
        photo = ImageTk.PhotoImage(pil_image)
        canvas_popup.config(width=processed_image.shape[1], height=processed_image.shape[0])  # Adjust canvas size
        canvas_popup.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas_popup.image = photo

    popup = tk.Toplevel(root)
    popup.title("Edit Image")

    # Resize image proportionally to 720px height
    def resize_image_proportionally(image, max_height=720):
        original_height, original_width = image.shape[:2]
        scaling_factor = max_height / original_height
        new_width = int(original_width * scaling_factor)
        resized_image = cv2.resize(image, (new_width, max_height))
        return resized_image

    # Resize the uploaded image before processing
    resized_uploaded_image = resize_image_proportionally(uploaded_image)

    popup.geometry(f"{resized_uploaded_image.shape[1] + 100}x{resized_uploaded_image.shape[0] + 200}")

    canvas_popup = tk.Canvas(popup)
    canvas_popup.pack(pady=10)

    ttk.Label(popup, text="Sensitivity").pack(pady=5)
    sensitivity_slider_popup = ttk.Scale(popup, from_=0, to=100, orient=tk.HORIZONTAL)
    sensitivity_slider_popup.set(30)
    sensitivity_slider_popup.pack(pady=10)
    sensitivity_slider_popup.bind("<Motion>", lambda event: update_popup_canvas(int(sensitivity_slider_popup.get())))

    def process_uploaded_image(sensitivity):
        if resized_uploaded_image is not None:
            gray = cv2.cvtColor(resized_uploaded_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, threshold1=sensitivity, threshold2=sensitivity * 3)
            line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            return line_drawing_frame

    def save_image():
        sensitivity = int(sensitivity_slider_popup.get())
        processed_image = process_uploaded_image(sensitivity)
        cv2.imwrite("line_drawing.png", processed_image)
        print("Image saved as line_drawing.png")
        popup.destroy()

    # Initial display
    update_popup_canvas(30)

    save_button = ttk.Button(popup, text="Save", command=save_image)
    save_button.pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("Camera Feed")

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

control_frame = tk.Frame(root)
control_frame.pack(side='top', pady=10, fill="x")

control_frame.columnconfigure([1, 3, 4, 5, 7, 8], weight=0)
control_frame.columnconfigure([2, 6], weight=1)

upload_button = ttk.Button(control_frame, text="Upload Image", command=upload_and_save)
upload_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

camera_list = detect_cameras()
selected_camera = StringVar(value="Select camera")
if camera_list:
    camera_names = [name for name, _ in camera_list]
    camera_menu = ttk.OptionMenu(
        control_frame, selected_camera, "Select camera", *camera_names,
        command=lambda _: change_camera(camera_list[camera_names.index(selected_camera.get())][1])
    )
    camera_menu.grid(row=1, column=3, padx=10, pady=10)

photo_button = ttk.Button(control_frame, text="Take Photo", command=capture_and_save)
photo_button.grid(row=1, column=4, padx=10, pady=10)

invert_button = ttk.Button(control_frame, text="Invert Camera", command=invert_camera)
invert_button.grid(row=1, column=5, padx=10, pady=10)

ttk.Label(control_frame, text="Sensitivity").grid(row=0, column=8, padx=5, pady=0, sticky="e")
sensitivity_slider = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL)
sensitivity_slider.set(30)
sensitivity_slider.grid(row=1, column=8, padx=10, pady=10, sticky="e")

if camera_list:
    change_camera(camera_list[0][1])

capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread.start()

update_camera()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
