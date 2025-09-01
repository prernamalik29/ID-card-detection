# Identity Card Detection

This project is designed to detect and extract information from various types of identity cards, such as Aadhaar, PAN, Passport, and Driving License, using image processing and deep learning techniques.

## Features
- Detects and extracts text from images of identity cards
- Supports multiple card types: Aadhaar, PAN, Passport, Driving License
- Utilizes pre-trained models for text detection and recognition
- GUI for easy interaction
- Web interface (Flask app)

## Project Structure
- `app.py`: Main Flask application for web interface
- `identification.py`, `identification_gui.py`, `id_gui.py`: Core logic and GUI scripts
- `model_files/`: Contains pre-trained model files
- `templates/`: HTML templates for web interface
- `uploads/`: Directory for uploaded images
- Various `.jpg` and `.png` files: Sample images for testing

## Requirements
- Python 3.8+
- OpenCV
- Flask
- Torch
- Other dependencies (see below)

## Installation
1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd identity_card_detection
   ```
2. Install required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not available, install manually:
   ```powershell
   pip install flask opencv-python torch torchvision
   ```
3. Place the pre-trained model files in the `model_files/` directory.

## Usage
### Run the Web App
```powershell
python app.py
```
Open your browser and go to `http://localhost:5000` to use the web interface.

### Run the GUI
```powershell
python identification_gui.py
```

## How It Works
- Upload an image of an identity card via the web or GUI.
- The system detects the card type and extracts relevant information using deep learning models.
- Results are displayed on the interface.

## Model Files
- `craft_mlt_25k.pth`: Text detection model
- `english_g2.pth`, `devanagari.pth`: Text recognition models for English and Devanagari scripts

## Sample Images
Sample images are provided in the root directory for testing purposes.

## License
This project is for educational and research purposes.
