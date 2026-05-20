from PIL import Image
import pytesseract

# Set path to Tesseract (if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust if necessary

# Open an image file (replace with the actual image filename in your folder)
image = Image.open(r'C:\Users\joshu\OneDrive\Documents\handwritten.jpeg')  # Replace this with the full path
 # Use the correct image file name
  # Replace this with the actual image name you have

# Perform OCR
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
