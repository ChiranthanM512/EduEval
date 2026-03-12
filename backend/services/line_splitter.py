import cv2
import numpy as np
import os


def split_into_lines(image_path: str, out_dir="uploads/lines"):
    """
    Splits paragraph image into line images for TrOCR
    """

    os.makedirs(out_dir, exist_ok=True)

    img = cv2.imread(image_path)

    if img is None:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # improve contrast
    gray = cv2.equalizeHist(gray)

    # binary image
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # clean noise
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    projection = np.sum(thresh, axis=1)

    lines = []
    start = None

    for i, val in enumerate(projection):

        if val > 50 and start is None:
            start = i

        elif val <= 50 and start is not None:
            end = i

            if end - start > 25:
                lines.append((start, end))

            start = None

    if start is not None:
        lines.append((start, len(projection) - 1))

    saved_paths = []

    line_index = 0

    for (y1, y2) in lines:

        crop = img[y1:y2, :]

        if crop.shape[0] < 20:
            continue

        save_path = os.path.join(out_dir, f"line_{line_index}.png")

        cv2.imwrite(save_path, crop)

        saved_paths.append(save_path)

        line_index += 1

    return saved_paths