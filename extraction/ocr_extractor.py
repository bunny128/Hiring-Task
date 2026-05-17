# extraction/ocr_extractor.py

import fitz
import numpy as np


class OCRExtractor:

    def __init__(self):
        from paddleocr import PaddleOCR

        self.ocr = PaddleOCR(use_angle_cls=True, lang="en")

    def extract_text_from_page(self, pdf_path, page_number):
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]
        pix = page.get_pixmap()

        img = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img.reshape(pix.height, pix.width, pix.n)

        result = self.ocr.ocr(img)
        extracted_text = []

        for line in result[0]:
            extracted_text.append(line[1][0])

        return "\n".join(extracted_text)
