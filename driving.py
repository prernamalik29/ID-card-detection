import re
import pytesseract
from PIL import Image

def detect_id_card(text):
    # Check for Aadhaar card patterns
    if re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text) or "आधार" in text or "AADHAAR" in text.upper():
        return "Aadhaar Card"
    
    # Check for PAN card patterns
    elif re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", text) or "INCOME TAX DEPARTMENT" in text or "PERMANENT ACCOUNT NUMBER" in text:
        return "PAN Card"
    
   # Check for Passport patterns
    elif re.search(r"[A-Z]{1}[0-9]{7}", text) or "PASSPORT" in text.upper() or "REPUBLIC OF INDIA" in text.upper() or "Government of India" in text:
        return "Passport"
    
    # Check for Driving License patterns
    elif re.search(r"[A-Z]{2}\d{2}\s?\d{11}\s?\d{4}", text) or "DRIVING LICENCE" in text.upper() or "DRIVING LICENSE" in text.upper():
        return "Driving License"
    
    # Check for Voter ID patterns
    elif re.search(r"[A-Z]{3}\d{7}", text) or "ELECTION COMMISSION OF INDIA" in text.upper() or "VOTER ID" in text.upper():
        return "Voter ID"
    
    else:
        return "Unknown ID Type"

def extract_id_info(image_path):
    # Load image
    img = Image.open(image_path)
    
    # Perform OCR
    text = pytesseract.image_to_string(img, lang='eng+hin')
    
    # Detect ID type
    id_type = detect_id_card(text)
    
    # Extract specific details based on ID type
    details = {}
    
    # Common date patterns in Indian ID cards
    date_patterns = [
        r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b\d{2}\.\d{2}\.\d{4}\b',      # DD.MM.YYYY
        r'\b\d{4}[/-]\d{2}[/-]\d{2}\b',  # YYYY/MM/DD or YYYY-MM-DD
        r'\bDOB[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})\b',  # DOB: DD/MM/YYYY
        r'\bDate of Birth[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})\b'  # Date of Birth: DD/MM/YYYY
    ]
    
    # Try to find date of birth using various patterns
    for pattern in date_patterns:
        dob_match = re.search(pattern, text, re.IGNORECASE)
        if dob_match:
            # Extract the date part from the match
            dob = dob_match.group(1) if len(dob_match.groups()) > 0 else dob_match.group(0)
            details["Date of Birth"] = dob
            break
    
    if id_type == "Aadhaar Card":
        aadhaar_no = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
        if aadhaar_no:
            details["Aadhaar Number"] = aadhaar_no.group()
    
    elif id_type == "PAN Card":
        pan_no = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", text)
        if pan_no:
            details["PAN Number"] = pan_no.group()
    
    elif id_type == "Passport":
        passport_no = re.search(r"[A-Z]{1}[0-9]{7}", text)
        if passport_no:
            details["Passport Number"] = passport_no.group()
    
    elif id_type == "Driving License":
        dl_no = re.search(r"[A-Z]{2}\d{2}\s?\d{11}\s?\d{4}", text)
        if dl_no:
            details["DL Number"] = dl_no.group()
    
    elif id_type == "Voter ID":
        voter_id = re.search(r"[A-Z]{3}\d{7}", text)
        if voter_id:
            details["Voter ID Number"] = voter_id.group()
    
    return {
        "ID Type": id_type,
        "Details": details,
        "Raw Text": text
    }

if __name__ == "__main__":
    result = extract_id_info("ac4.jpg")
    print("--------------------------------")
    print(f"Detected ID Type: {result['ID Type']}")
    print("--------------------------------")
    print("Extracted Details:")
    for key, value in result['Details'].items():
        print(f"{key}: {value}")
