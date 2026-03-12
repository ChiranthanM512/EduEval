import torch
import easyocr
import cv2
import os
import numpy as np
from pathlib import Path
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from services.line_splitter import split_into_lines

try:
    from services.pdf_to_images import pdf_to_images
except ImportError:
    def pdf_to_images(path):
        return [path]

from services.config import EASY_OCR_CONFIDENCE_THRESHOLD


class HybridOCR:

    def __init__(self):

        print("Initializing Hybrid OCR...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading TrOCR on {self.device}...")

        self.processor = TrOCRProcessor.from_pretrained(
            "microsoft/trocr-base-handwritten"
        )

        self.model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-handwritten"
        )

        self.model.to(self.device)

        print("Loading EasyOCR readers...")

        gpu_bool = torch.cuda.is_available()

        language_configs = {
            "english": ["en"],
            "tamil": ["ta", "en"],
            "hindi": ["hi", "en"],
            "telugu": ["te", "en"],
            "kannada": ["kn", "en"],
            "marathi": ["mr", "en"],
            "bengali": ["bn", "en"]
        }

        self.easy_readers = {}

        for lang, langs in language_configs.items():

            try:

                reader = easyocr.Reader(langs, gpu=gpu_bool)
                self.easy_readers[lang] = reader
                print(f"  ✅ EasyOCR loaded: {lang}")

            except Exception as e:

                print(f"  ⚠️ Skipping {lang} reader: {e}")

        print("OCR initialization complete")


    def preprocess(self, image_path):

        img = cv2.imread(str(image_path))

        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.equalizeHist(gray)

        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        return blur


    def preprocess_hindi(self, image_path):
        """
        VERY LIGHT preprocessing for Devanagari (Hindi) handwritten text.
        EasyOCR handles most of the image preprocessing internally — aggressive
        thresholding breaks matras (vowel marks) and merges characters.
        This function only scales up small images for better character resolution.
        """
        img = cv2.imread(str(image_path))
        if img is None:
            return None

        h, w = img.shape[:2]

        # If image is small, upscale for better Devanagari character resolution
        if w < 1000:
            scale = 1000.0 / w
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        return img


    def trocr_read_line(self, image_path):

        try:

            image = Image.open(image_path).convert("RGB")

            pixel_values = self.processor(
                images=image,
                return_tensors="pt"
            ).pixel_values.to(self.device)

            ids = self.model.generate(
                pixel_values,
                max_new_tokens=60,
                num_beams=5,
                length_penalty=1.0,
                early_stopping=True
            )

            text = self.processor.batch_decode(
                ids,
                skip_special_tokens=True
            )[0]

            return text.strip()

        except Exception as e:

            print("TrOCR error:", e)

            return ""


    def trocr_paragraph(self, image_path):
        """
        Robust strategy: Use EasyOCR to detect boxes, group them into lines by Y-overlap,
        sort lines by Y, sort boxes within lines by X, and feed to TrOCR.
        """
        img = cv2.imread(str(image_path))
        if img is None:
            return ""

        reader = self.easy_readers.get("english")
        if reader is None:
            reader = next(iter(self.easy_readers.values()), None)

        if not reader:
            return ""

        raw_results = reader.readtext(img)
        if not raw_results:
            return ""

        items = []
        for res in raw_results:
            box = res[0]
            y_coords = [p[1] for p in box]
            x_coords = [p[0] for p in box]
            items.append({
                "box": box,
                "y_min": min(y_coords),
                "y_max": max(y_coords),
                "y_mid": sum(y_coords) / len(y_coords),
                "x_mid": sum(x_coords) / len(x_coords)
            })

        items.sort(key=lambda x: x["y_mid"])
        
        lines = []
        if items:
            current_line = [items[0]]
            for i in range(1, len(items)):
                avg_y_min = sum(it["y_min"] for it in current_line) / len(current_line)
                avg_y_max = sum(it["y_max"] for it in current_line) / len(current_line)
                h = max(1.0, avg_y_max - avg_y_min)
                
                overlap_min = max(float(items[i]["y_min"]), float(avg_y_min))
                overlap_max = min(float(items[i]["y_max"]), float(avg_y_max))
                overlap = max(0.0, overlap_max - overlap_min)
                
                if overlap > 0.4 * h:
                    current_line.append(items[i])
                else:
                    lines.append(current_line)
                    current_line = [items[i]]
            lines.append(current_line)

        for line in lines:
            line.sort(key=lambda x: x["x_mid"])

        combined_text = []
        os.makedirs("uploads", exist_ok=True)
        h_img, w_img, _ = img.shape

        for line_idx, line in enumerate(lines):
            line_parts = []
            for item_idx, item in enumerate(line):
                box = item["box"]
                y1, y2 = int(item["y_min"]), int(item["y_max"])
                x1, x2 = int(min(p[0] for p in box)), int(max(p[0] for p in box))

                y1, y2 = max(0, y1-10), min(h_img, y2+10)
                x1, x2 = max(0, x1-10), min(w_img, x2+10)

                if y2 - y1 < 5 or x2 - x1 < 5:
                    continue

                crop = img[y1:y2, x1:x2]
                temp_path = f"uploads/temp_line_{line_idx}_{item_idx}.png"
                cv2.imwrite(temp_path, crop)

                text = self.trocr_read_line(temp_path)
                if text.strip():
                    line_parts.append(text)
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            if line_parts:
                combined_text.append(" ".join(line_parts))

        return "\n".join(combined_text)

    def detect_dominant_language(self, text):
        if not text:
            return "english"
        
        devanagari_count = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        tamil_count = sum(1 for c in text if '\u0B80' <= c <= '\u0BFF')
        telugu_count = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
        kannada_count = sum(1 for c in text if '\u0C80' <= c <= '\u0CFF')
        bengali_count = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
        english_count = sum(1 for c in text if 'a' <= c.lower() <= 'z')

        counts = {
            "hindi": devanagari_count,
            "tamil": tamil_count,
            "telugu": telugu_count,
            "kannada": kannada_count,
            "bengali": bengali_count,
            "english": english_count
        }
        
        best_lang = max(counts.items(), key=lambda item: item[1])[0]
        if counts[best_lang] > 10:
            return best_lang
        return "english"

    def extract_paragraph_easyocr(self, image_path, lang="english"):
        """
        EasyOCR extraction with:
        - Confidence filtering to discard low-quality detections
        - Y-overlap line grouping (wider tolerance for Devanagari)
        - X-min sorting within line for correct left-to-right reading order
        """
        # Use Hindi-optimised preprocessing for Devanagari
        if lang == "hindi":
            processed = self.preprocess_hindi(image_path)
            if processed is not None:
                img = processed
            else:
                img = cv2.imread(str(image_path))
        else:
            img = cv2.imread(str(image_path))

        if img is None:
            return ""

        reader = self.easy_readers.get(lang)
        if reader is None:
            reader = next(iter(self.easy_readers.values()), None)
        if not reader:
            return ""

        # paragraph=True groups nearby text — better for dense handwriting
        # For Hindi: pass the IMAGE PATH directly (not numpy array) so EasyOCR
        # uses its own internal Devanagari-optimised preprocessing pipeline.
        if lang == "hindi":
            raw_results = reader.readtext(
                str(image_path),   # original file path, NOT the preprocessed array
                detail=1,
                min_size=15
            )
        else:
            raw_results = reader.readtext(
                img,
                detail=1,
                min_size=10
            )
        if not raw_results:
            return ""

        # Confidence threshold — Devanagari naturally scores lower, so be lenient
        CONF_THRESHOLD = 0.25

        items = []
        for res in raw_results:
            box, text, conf = res[0], str(res[1]), float(res[2])
            if conf < CONF_THRESHOLD or not text.strip():
                continue
            y_coords = [p[1] for p in box]
            x_coords = [p[0] for p in box]
            items.append({
                "text": text,
                "conf": conf,
                "y_min": min(y_coords),
                "y_max": max(y_coords),
                "y_mid": sum(y_coords) / len(y_coords),
                "x_min": min(x_coords),   # Use x_min for proper L-R ordering
                "x_mid": sum(x_coords) / len(x_coords)
            })

        if not items:
            return ""

        items.sort(key=lambda x: x["y_mid"])

        # Line grouping — use 50% overlap tolerance (wider than default 40%)
        # This helps keep Devanagari matras/vowels joined to their base consonants
        lines = []
        current_line = [items[0]]
        for i in range(1, len(items)):
            avg_y_min = sum(it["y_min"] for it in current_line) / len(current_line)
            avg_y_max = sum(it["y_max"] for it in current_line) / len(current_line)
            h = max(1.0, avg_y_max - avg_y_min)

            overlap = max(
                0.0,
                min(float(items[i]["y_max"]), float(avg_y_max))
                - max(float(items[i]["y_min"]), float(avg_y_min))
            )

            if overlap > 0.35 * h:
                current_line.append(items[i])
            else:
                lines.append(current_line)
                current_line = [items[i]]
        lines.append(current_line)

        combined_text = []
        for line in lines:
            # Sort by x_min for correct reading order within each line
            line.sort(key=lambda x: x["x_min"])
            parts = [item["text"].strip() for item in line if item["text"].strip()]
            if parts:
                combined_text.append(" ".join(parts))

        return "\n".join(combined_text)


    def easy_read(self, processed_img, reader_key):

        reader = self.easy_readers.get(reader_key)

        if not reader:
            return ""

        try:

            result = reader.readtext(processed_img)

            texts = [r[1] for r in result]

            return " ".join(texts)

        except Exception as e:

            print("EasyOCR error:", e)

            return ""


    def extract_text_from_image(self, image_path, hint_text=""):

        lang_hint = self.detect_dominant_language(hint_text)

        if lang_hint == "english":
            trocr_text = self.trocr_paragraph(image_path)
            if trocr_text.strip():
                return trocr_text
            processed = self.preprocess(image_path)
            return self.easy_read(processed, "english")

        # For Hindi and other Indic scripts — use dedicated EasyOCR reader
        # TrOCR is NOT used here (English-only model).
        if lang_hint in ("hindi", "tamil", "telugu", "kannada", "marathi", "bengali"):
            return self.extract_paragraph_easyocr(image_path, lang=lang_hint)

        return self.extract_paragraph_easyocr(image_path, lang=lang_hint)


    def extract_text(self, file_path, hint_text=""):

        path = Path(file_path)

        if path.suffix.lower() == ".pdf":

            images = pdf_to_images(file_path)

            results = []

            for img in images:

                text = self.extract_text_from_image(img, hint_text)

                if text.strip():
                    results.append(text)

            return "\n".join(results)

        return self.extract_text_from_image(file_path, hint_text)


hybrid_ocr = HybridOCR()