import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from identification import extract_id_info

class IDVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Card Verification System")
        self.root.geometry("1200x800")
        
        # Store uploaded images and their extracted information
        self.uploaded_images = []
        self.extracted_info = []
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload buttons
        self.upload_frame = ttk.LabelFrame(self.main_frame, text="Upload ID Cards", padding="10")
        self.upload_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(self.upload_frame, text="Upload ID Card", command=self.upload_image).grid(row=0, column=0, padx=5)
        ttk.Button(self.upload_frame, text="Verify IDs", command=self.verify_ids).grid(row=0, column=1, padx=5)
        ttk.Button(self.upload_frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=5)
        
        # Create scrollable frames
        self.create_scrollable_frames()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
    def create_scrollable_frames(self):
        # Image display area with scrollbar
        self.image_frame = ttk.LabelFrame(self.main_frame, text="Uploaded Images", padding="10")
        self.image_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create canvas and scrollbar for images
        self.image_canvas = tk.Canvas(self.image_frame)
        self.image_scrollbar = ttk.Scrollbar(self.image_frame, orient="vertical", command=self.image_canvas.yview)
        self.image_scrollable_frame = ttk.Frame(self.image_canvas)
        
        self.image_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
        )
        self.image_canvas.create_window((0, 0), window=self.image_scrollable_frame, anchor="nw")
        self.image_canvas.configure(yscrollcommand=self.image_scrollbar.set)
        
        self.image_canvas.pack(side="left", fill="both", expand=True)
        self.image_scrollbar.pack(side="right", fill="y")
        
        # Results area with scrollbar
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Verification Results", padding="10")
        self.results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create canvas and scrollbar for results
        self.results_canvas = tk.Canvas(self.results_frame)
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_scrollable_frame = ttk.Frame(self.results_canvas)
        
        self.results_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        
        self.results_canvas.pack(side="left", fill="both", expand=True)
        self.results_scrollbar.pack(side="right", fill="y")
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            # Extract information from the image
            try:
                result = extract_id_info(file_path)
                
                # Store the image and its information
                self.uploaded_images.append(file_path)
                self.extracted_info.append(result)
                
                # Display the image
                self.display_image(file_path)
                
                # Display extracted information
                self.display_info(result)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
    
    def display_image(self, image_path):
        # Create a frame for the new image
        img_frame = ttk.Frame(self.image_scrollable_frame)
        img_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        try:
            # Load and resize image
            img = Image.open(image_path)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Display image
            label = ttk.Label(img_frame, image=photo)
            label.image = photo  # Keep a reference
            label.pack()
            
            # Add image path label
            ttk.Label(img_frame, text=os.path.basename(image_path)).pack()
        except Exception as e:
            ttk.Label(img_frame, text=f"Error loading image: {os.path.basename(image_path)}").pack()
    
    def display_info(self, info):
        # Create a frame for the information
        info_frame = ttk.Frame(self.results_scrollable_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Display ID type
        ttk.Label(info_frame, text=f"ID Type: {info.get('ID Type', 'Unknown')}", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Display extracted details
        details = info.get('Details', {})
        for key, value in details.items():
            ttk.Label(info_frame, text=f"{key}: {value}").pack(anchor=tk.W)
        
        ttk.Separator(info_frame, orient='horizontal').pack(fill='x', pady=5)
    
    def verify_ids(self):
        if len(self.extracted_info) < 2:
            messagebox.showwarning("Warning", "Please upload at least 2 ID cards for verification")
            return
        
        # Clear previous verification results
        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Compare all pairs of IDs
        all_comparisons = []
        for i in range(len(self.extracted_info)):
            for j in range(i + 1, len(self.extracted_info)):
                comparison = self.compare_info(self.extracted_info[i], self.extracted_info[j])
                all_comparisons.append(comparison)
                self.display_comparison(self.extracted_info[i], self.extracted_info[j], comparison)
        
        # Determine overall verification result
        overall_result = self.determine_overall_result(all_comparisons)
        
        # Display overall verification result at the top of results
        result_frame = ttk.Frame(self.results_scrollable_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        if overall_result == "match":
            result_text = "✅ All ID cards belong to the same person!"
            color = "green"
        elif overall_result == "partial":
            result_text = "⚠️ Some ID cards match but not all. Please review carefully."
            color = "orange"
        else:
            result_text = "❌ ID cards do not belong to the same person!"
            color = "red"
            
        ttk.Label(result_frame, text=result_text, font=('Arial', 12, 'bold'), foreground=color).pack(anchor=tk.W)
        ttk.Separator(result_frame, orient='horizontal').pack(fill='x', pady=5)
    
    def compare_info(self, info1, info2):
        comparison = {
            'name_match': False,
            'dob_match': False,
            'gender_match': False,
            'other_matches': [],
            'total_fields': 0,
            'matching_fields': 0
        }
        
        # Helper function to clean and standardize values
        def clean_value(value):
            if not value:
                return ""
            return ' '.join(str(value).strip().upper().split())
        
        # Compare name
        name1 = clean_value(info1.get('Details', {}).get('Name'))
        name2 = clean_value(info2.get('Details', {}).get('Name'))
        if name1 and name2:
            comparison['total_fields'] += 1
            comparison['name_match'] = name1 == name2
            if comparison['name_match']:
                comparison['matching_fields'] += 1
        
        # Compare date of birth
        dob1 = clean_value(info1.get('Details', {}).get('Date of Birth'))
        dob2 = clean_value(info2.get('Details', {}).get('Date of Birth'))
        if dob1 and dob2:
            comparison['total_fields'] += 1
            # Simple date comparison (for more robust comparison, use date parsing)
            comparison['dob_match'] = dob1 == dob2
            if comparison['dob_match']:
                comparison['matching_fields'] += 1
        
        # Compare gender
        gender1 = clean_value(info1.get('Details', {}).get('Gender'))
        gender2 = clean_value(info2.get('Details', {}).get('Gender'))
        if gender1 and gender2:
            comparison['total_fields'] += 1
            # Standardize gender representations
            gender1 = gender1[:1]  # Take first character (M/F)
            gender2 = gender2[:1]
            comparison['gender_match'] = gender1 == gender2
            if comparison['gender_match']:
                comparison['matching_fields'] += 1
        
        # Compare other fields
        details1 = info1.get('Details', {})
        details2 = info2.get('Details', {})
        all_keys = set(details1.keys()).union(set(details2.keys()))
        
        for key in all_keys:
            if key not in ['Name', 'Date of Birth', 'Gender']:
                val1 = clean_value(details1.get(key))
                val2 = clean_value(details2.get(key))
                if val1 and val2:
                    comparison['total_fields'] += 1
                    match = val1 == val2
                    comparison['other_matches'].append((key, match))
                    if match:
                        comparison['matching_fields'] += 1
        
        return comparison
    
    def display_comparison(self, info1, info2, comparison):
        # Create a frame for the comparison
        comp_frame = ttk.LabelFrame(self.results_scrollable_frame, 
                                  text=f"Comparing {info1.get('ID Type', 'ID 1')} with {info2.get('ID Type', 'ID 2')}")
        comp_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Only show if there's at least one match
        if comparison['matching_fields'] > 0:
            pair_status = "✅ ID cards belong to the same person"
            color = "green"
        else:
            pair_status = "❌ ID cards do not belong to the same person"
            color = "red"
            
        ttk.Label(comp_frame, text=pair_status, font=('Arial', 12, 'bold'), foreground=color).pack(anchor=tk.W)
        ttk.Separator(comp_frame, orient='horizontal').pack(fill='x', pady=5)
    
    def determine_overall_result(self, all_comparisons):
        if not all_comparisons:
            return "no_match"
        
        # If any comparison has at least one matching field, consider it a match
        for comp in all_comparisons:
            if comp['matching_fields'] > 0:
                return "match"
        
        return "no_match"
    
    def clear_all(self):
        # Clear all stored data
        self.uploaded_images = []
        self.extracted_info = []
        
        # Clear all displayed widgets
        for widget in self.image_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IDVerificationApp(root)
    root.mainloop()