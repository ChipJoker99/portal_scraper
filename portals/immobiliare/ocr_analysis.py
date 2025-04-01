import pytesseract
from PIL import Image
import sys

def extract_text(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, config='--psm 6 digits')
        return text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    extracted_text = extract_text(image_path)
    if extracted_text:
        print(f"Extracted Text: {extracted_text}")
    else:
        print("Failed to extract text.")