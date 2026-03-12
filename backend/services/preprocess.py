import cv2
import numpy as np

def preprocess_for_ocr(image_path: str) -> str:
    img = cv2.imread(image_path)

    if img is None:
        return image_path

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    # Denoise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Threshold (make handwriting darker)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # Save processed image
    out_path = image_path.replace(".", "_clean.")
    cv2.imwrite(out_path, thresh)

    return out_path
