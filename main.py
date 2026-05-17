# main.py

import argparse

from processing.heading_detector import HeadingDetector
from processing.classifier import SectionClassifier
from processing.page_range_detector import PageRangeDetector

from utils.text_cleaner import clean_text
from output.formatter import format_output

from config import MIN_TEXT_THRESHOLD


PDF_PATH = "sample_tender.pdf"


def main(pdf_path=PDF_PATH):
    from extraction.pdf_extractor import PDFExtractor
    from extraction.ocr_extractor import OCRExtractor

    pdf_extractor = PDFExtractor(pdf_path)
    ocr_extractor = None

    heading_detector = HeadingDetector()

    classifier = SectionClassifier()

    page_range_detector = PageRangeDetector()

    pages = pdf_extractor.extract_page_text()

    total_pages = len(pages)

    for page in pages:

        page_num = page["page_num"]

        text = page["text"]

        # OCR fallback
        if len(text.strip()) < MIN_TEXT_THRESHOLD:
            if ocr_extractor is None:
                ocr_extractor = OCRExtractor()

            text = ocr_extractor.extract_text_from_page(
                pdf_path,
                page_num
            )

        text = clean_text(text)

        heading = heading_detector.detect_heading(text)

        section_metadata = classifier.extract_section(heading)

        if section_metadata:

            section = {
                "type": section_metadata["type"],
                "identifier": section_metadata["identifier"],
                "title": section_metadata["title"],
                "start_page": page_num,
                "end_page": None
            }

            page_range_detector.add_section(section)

    final_sections = page_range_detector.finalize(total_pages)

    print(format_output(final_sections))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract Form and Annexure page ranges from a tender PDF."
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=PDF_PATH,
        help="Path to the tender PDF."
    )

    args = parser.parse_args()

    main(args.pdf_path)
