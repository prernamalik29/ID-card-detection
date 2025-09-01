import tkinter as tk
from tkinter import ttk
from identification import extract_id_info
import os

def test_display():
    root = tk.Tk()
    root.title("Test ID Card Display")
    root.geometry("600x400")
    
    # Test with a known image file
    test_image = "ac4.jpg"  # This should be one of your test images
    
    if os.path.exists(test_image):
        try:
            # Extract information using identification.py
            result = extract_id_info(test_image)
            
            # Display the results
            title = ttk.Label(root, text="Test Results from identification.py", font=("Arial", 14, "bold"))
            title.pack(pady=20)
            
            # Display ID Type
            id_type_label = ttk.Label(root, text=f"Detected ID Type: {result['ID Type']}", 
                                    font=("Arial", 12, "bold"), foreground="blue")
            id_type_label.pack(pady=10)
            
            # Display separator
            separator = ttk.Separator(root, orient='horizontal')
            separator.pack(fill='x', pady=10)
            
            # Display extracted details
            details_label = ttk.Label(root, text="Extracted Details:", font=("Arial", 11, "bold"))
            details_label.pack(pady=5)
            
            for key, value in result['Details'].items():
                detail = ttk.Label(root, text=f"{key}: {value}", font=("Consolas", 11))
                detail.pack(pady=2)
            
            # Display raw text (first 200 characters)
            raw_text = result.get('Raw Text', '')[:200] + "..." if len(result.get('Raw Text', '')) > 200 else result.get('Raw Text', '')
            raw_label = ttk.Label(root, text=f"Raw Text (first 200 chars): {raw_text}", 
                                font=("Consolas", 9), wraplength=550)
            raw_label.pack(pady=10)
            
        except Exception as e:
            error_label = ttk.Label(root, text=f"Error: {str(e)}", foreground="red")
            error_label.pack(pady=20)
    else:
        error_label = ttk.Label(root, text=f"Test image {test_image} not found", foreground="red")
        error_label.pack(pady=20)
    
    # Close button
    close_btn = ttk.Button(root, text="Close", command=root.destroy)
    close_btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_display() 