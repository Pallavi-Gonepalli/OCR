# ocr_engine.py

import pytesseract
import cv2

def extract_text_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale for better OCR results
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to clean the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Run OCR using pytesseract
    text = pytesseract.image_to_string(thresh)

    return text
