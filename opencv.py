import cv2
import matplotlib.pyplot as plt

# Load the image (replace 'your_image.jpg' with your actual image file name)
img = cv2.imread(r"iii.jpg")


# Check if image loaded correctly
if img is None:
    print("Image not found. Check the file name and path.")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the Haar cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles on detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display image with faces
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Detected Faces")
    plt.show()
