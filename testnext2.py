import cv2
from PIL import Image, ImageTk
import os
from identification import extract_id_info
import re
from test import IDVerificationApp
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class SimpleIDCardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Identity Card Detection & Verification")
        self.root.geometry("800x700")
        self.uploaded_file = None
        self.result = None
        self.extractor = None
        self.init_extractor()
        self.create_widgets()

    def init_extractor(self):
        def init():
            try:
                self.extractor = Extractor()
            except Exception as e:
                print(f"Error initializing extractor: {e}")
        thread = threading.Thread(target=init)
        thread.daemon = True
        thread.start()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Identity Card Detection & Verification", font=("Arial", 18, "bold"))
        title.pack(pady=(20, 10))

        # Upload area frame
        upload_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, bg="#f8f8ff", height=200, width=600)
        upload_frame.pack(pady=10)
        upload_frame.pack_propagate(False)
        self.upload_frame = upload_frame

        # Upload icon and text
        icon = ttk.Label(upload_frame, text="📄", font=("Arial", 48))
        icon.pack(pady=(20, 0))
        upload_text = ttk.Label(upload_frame, text="Browse or Drag & Drop your files here", font=("Arial", 12))
        upload_text.pack(pady=(10, 0))
        formats = ttk.Label(upload_frame, text="Supported formats: PDF, JPEG", font=("Arial", 10, "italic"))
        formats.pack(pady=(0, 10))
        browse_btn = ttk.Button(upload_frame, text="Browse", command=self.browse_file)
        browse_btn.pack()
        upload_frame.bind("<Button-1>", lambda e: self.browse_file())

        # File name label
        self.file_label = ttk.Label(self.root, text="", font=("Arial", 10))
        self.file_label.pack(pady=(5, 0))

        # Process button
        self.process_btn = ttk.Button(self.root, text="Process", command=self.process_file, state=tk.DISABLED)
        self.process_btn.pack(pady=20)

        # Results area with scrollbar
        results_container = tk.Frame(self.root)
        results_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        self.results_canvas = tk.Canvas(results_container, borderwidth=0)
        self.results_scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=self.results_canvas.yview)
        self.results_frame = tk.Frame(self.results_canvas)
        self.results_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_canvas.pack(side="left", fill="both", expand=True)
        self.results_scrollbar.pack(side="right", fill="y")
        self.results_widgets = []

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("PDF files", "*.pdf")])
        if file_path:
            self.uploaded_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.process_btn.config(state=tk.NORMAL)
            self.clear_results()

    def process_file(self):
        self.clear_results()
        if not self.uploaded_file:
            messagebox.showwarning("No file", "Please upload a file first.")
            return
        ext = os.path.splitext(self.uploaded_file)[-1].lower()
        is_image = ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        is_pdf = ext == ".pdf"

        # Section: Number of ID cards detected
        num_cards = 0
        faces = []
        if is_image:
            img = cv2.imread(self.uploaded_file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            num_cards = len(faces)
        num_label = ttk.Label(self.results_frame, text=f"Number of ID cards detected: {num_cards if is_image else 'N/A'}", font=("Arial", 12, "bold"))
        num_label.pack(anchor=tk.W, pady=(0, 10))
        self.results_widgets.append(num_label)
        # Checklist
        accessible = os.path.exists(self.uploaded_file)
        self.show_result_row("Confirm that the document is uploaded and accessible.", accessible)
        expected_format = is_image or is_pdf
        self.show_result_row("Check if the document is in the expected format (e.g. PDF, image, scanned document).", expected_format)
        
        # Extract details using identification.py for each detected card
        infos = []
        if is_image and num_cards > 0:
            img = cv2.imread(self.uploaded_file)
            for idx, (x, y, w, h) in enumerate(faces):
                face_img = img[y:y+h, x:x+w]
                temp_path = f"_temp_face_{x}_{y}.jpg"
                cv2.imwrite(temp_path, face_img)
                try:
                    info = extract_id_info(temp_path)
                    infos.append(info)
                except Exception as e:
                    infos.append({'Details': {'Error': str(e)}})
                os.remove(temp_path)
        else:
            try:
                info = extract_id_info(self.uploaded_file)
                infos.append(info)
            except Exception as e:
                infos.append({'Details': {'Error': str(e)}})
        
        # Checklist: Verify document type
        doc_type_verified = all(info.get('ID Type', 'Unknown') != 'Unknown' for info in infos)
        self.show_result_row("Verify the document type (e.g., identity document, driving licence, etc.)", doc_type_verified)
        # Checklist: Verify all mandatory fields present
        all_fields_present = all(bool(info.get('Details')) for info in infos)
        self.show_result_row("Verify that all mandatory sections/fields are present in the document.", all_fields_present)
        # Checklist: Check for blank/incomplete fields
        no_blank_fields = all(all(bool(v) for v in info.get('Details', {}).values()) for info in infos)
        self.show_result_row("Check for any blank or incomplete fields that require input.", no_blank_fields)
        # Show extracted info for each card
        for idx, info in enumerate(infos):
            details = info.get('Details', {})
            id_type = info.get('ID Type', 'Unknown')
            # Build the output string exactly as in the terminal
            output_lines = [
                f"Detected ID Type: {id_type}",
                "--------------------------------",
                "Extracted Details:"
            ]
            for k, v in details.items():
                output_lines.append(f"{k}: {v}")
            output_str = "\n".join(output_lines)
            # Show as a single block in a monospaced font
            details_label = tk.Label(self.results_frame, text=output_str, font=("Consolas", 11), justify="left", anchor="w")
            details_label.pack(anchor=tk.W, pady=(10, 0))
            self.results_widgets.append(details_label)

    def show_result_row(self, text, passed):
        row = ttk.Frame(self.results_frame)
        row.pack(fill=tk.X, pady=2)
        label = ttk.Label(row, text=text, font=("Arial", 11))
        label.pack(side=tk.LEFT, anchor=tk.W)
        status = ttk.Label(row, text="✔" if passed else "✖", foreground="green" if passed else "red", font=("Arial", 14, "bold"))
        status.pack(side=tk.RIGHT)
        self.results_widgets.append(row)

    def show_extracted_info(self, details):
        if not details:
            return
        sep = ttk.Separator(self.results_frame, orient='horizontal')
        sep.pack(fill='x', pady=8)
        self.results_widgets.append(sep)
        info_title = ttk.Label(self.results_frame, text="Extracted Information:", font=("Arial", 12, "bold"))
        info_title.pack(anchor=tk.W)
        self.results_widgets.append(info_title)
        for k, v in details.items():
            info = ttk.Label(self.results_frame, text=f"{k}: {v}", font=("Arial", 11))
            info.pack(anchor=tk.W)
            self.results_widgets.append(info)

    def clear_results(self):
        for w in self.results_widgets:
            w.destroy()
        self.results_widgets = []

class Extractor:
    def __init__(self):
        self._hidden_root = tk.Tk()
        self._hidden_root.withdraw()
        self.app = IDVerificationApp(self._hidden_root)
    def extract(self, path):
        return self.app.extract_id_info(path)
    def compare(self, info1, info2):
        return self.app.compare_info(info1, info2)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleIDCardGUI(root)
    root.mainloop()