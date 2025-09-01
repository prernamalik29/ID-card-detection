import cv2
import pytesseract
import re

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\DELL\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract"

def is_pan_card(image_path):
    # Load image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Extract text
    text = pytesseract.image_to_string(thresh, lang='eng')
    
    # Common PAN card identifiers
    pan_identifiers = [
        "INCOME TAX DEPARTMENT",
        "GOVT. OF INDIA",
        "GOVERNMENT OF INDIA",
        "PERMANENT ACCOUNT NUMBER",
        "Permanent Account Number",
        "PAN CARD"
    ]
    
    # Check for any PAN card identifier
    is_pan = any(identifier in text for identifier in pan_identifiers)
    
    # Try to extract PAN number (format: ABCDE1234F)
    pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    
    if is_pan:
        print("Document is a PAN CARD")
        if pan_match:
            print("PAN Number:", pan_match.group(0))
        else:
            print("PAN Number: Not found or not in standard format")
        return True
    else:
        print("PAN CARD not detected")
        return False

# Test the function
is_pan_card("pc.jpg")
