import pytesseract
import cv2
import re

# Set Tesseract path (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\DELL\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract"

# Read Aadhaar image
image = cv2.imread('aaa.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Improve OCR accuracy by preprocessing
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Extract text using Tesseract
text = pytesseract.image_to_string(thresh)

# Clean and split text into lines
lines = [line.strip() for line in text.split('\n') if line.strip()]

# Find the name (usually the first or second line)
name = None
for line in lines[:5]:  # Check first 5 lines (Aadhaar name is usually at the top)
    # Match valid name (exclude numbers, symbols, and Aadhaar keywords)
    if re.match(r'^[A-Za-z\s]+$', line) and "aadhaar" not in line.lower() and "male" not in line.lower() and "female" not in line.lower():
        name = line
        break

print("Extracted Name:", name)

