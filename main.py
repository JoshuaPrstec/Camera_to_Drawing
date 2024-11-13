import cv2
import tkinter as tk
from tkinter import Canvas, StringVar, ttk
from PIL import Image, ImageTk
import threading
import gc
import time

is_inverted = True
cap = None
current_camera_index = None
stop_event = threading.Event()
cap_lock = threading.Lock()

def detect_cameras():
    camera_list = []
    for i in range(10):
        temp_cap = cv2.VideoCapture(i)
        if temp_cap.isOpened():
            camera_list.append((f"Camera {i}", i))
            temp_cap.release()
    return camera_list

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

def capture_and_save():
    def capture():
        with cap_lock:
            if cap is not None:
                ret, frame = cap.read()
                if ret:
                    if is_inverted:
                        frame = cv2.flip(frame, 1)
                    # Process and save the image in a new thread to keep UI responsive
                    threading.Thread(target=process_and_save_image, args=(frame,)).start()

    threading.Thread(target=capture).start()

def process_and_save_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=sensitivity_slider.get(), threshold2=sensitivity_slider.get() * 3)
    line_drawing_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    resized_image = cv2.resize(line_drawing_frame, (640, 360))
    cv2.imwrite("captured_image_with_filter.png", resized_image)
    print("Image captured and saved as captured_image_with_filter.png")
    gc.collect()

def invert_camera():
    global is_inverted
    is_inverted = not is_inverted

def update_camera():
    while not stop_event.is_set():
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
                    canvas.create_image((canvas.winfo_width() - photo.width()) // 2, (canvas.winfo_height() - photo.height()) // 2, image=photo, anchor=tk.NW)
                    canvas.image = photo
        time.sleep(0.03)

root = tk.Tk()
root.title("Camera Feed")

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

selected_camera = StringVar(value="Select camera")
control_frame = tk.Frame(root)
control_frame.pack(side='bottom', pady=20)

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")
style.configure("TOptionMenu", padding=6, relief="flat", background="#ccc")

camera_list = detect_cameras()
if camera_list:
    camera_names = [name for name, _ in camera_list]
    camera_menu = ttk.OptionMenu(control_frame, selected_camera, "Select camera", *camera_names, command=lambda _: threading.Thread(target=change_camera, args=(camera_list[camera_names.index(selected_camera.get())][1],)).start())
    camera_menu.grid(row=0, column=0, padx=10, pady=10)

photo_button = ttk.Button(control_frame, text="Take Photo", command=capture_and_save)
photo_button.grid(row=0, column=1, padx=10, pady=10)

invert_button = ttk.Button(control_frame, text="Invert Camera", command=invert_camera)
invert_button.grid(row=0, column=2, padx=10, pady=10)

sensitivity_slider = ttk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL)
sensitivity_slider.set(30)
sensitivity_slider.grid(row=0, column=3, padx=10, pady=10)
ttk.Label(control_frame, text="Sensitivity").grid(row=0, column=4, padx=10, pady=10)

if camera_list:
    cap = cv2.VideoCapture(camera_list[0][1])
    if cap.isOpened():
        current_camera_index = camera_list[0][1]
        threading.Thread(target=update_camera, daemon=True).start()

def on_closing():
    stop_event.set()
    if cap is not None:
        cap.release()
    root.destroy()
    gc.collect()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

stop_event.set()
if cap is not None:
    cap.release()
gc.collect()
