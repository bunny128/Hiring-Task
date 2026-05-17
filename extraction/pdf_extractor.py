# extraction/pdf_extractor.py

import fitz


class PDFExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def extract_page_text(self):
        pages = []

        for page_num, page in enumerate(self.doc, start=1):
            pages.append({
                "page_num": page_num,
                "text": page.get_text()
            })

        return pages
