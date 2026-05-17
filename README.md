# Tender Form and Annexure Parser

This project extracts the list of Forms and Annexures from a tender PDF and returns only their metadata:

- type: `Form` or `Annexure`
- name: for example `Form 1` or `Annexure A`
- title: heading/title as detected from the document
- pages: inferred page range

It does not extract the data inside the forms or annexures. That can be added as the next stage after reliable section detection.

## Expected Output

```json
[
  {
    "type": "Form",
    "name": "Form 1",
    "title": "Bid Submission Form",
    "pages": "1-5"
  },
  {
    "type": "Annexure",
    "name": "Annexure A",
    "title": "Technical Specifications",
    "pages": "20-25"
  }
]
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the parser:

```bash
python3 main.py "sample pdf/Tender.pdf"
```

You can also pass any tender PDF path:

```bash
python3 main.py "/path/to/tender.pdf"
```

## Approach / Pipeline Design

The solution follows a simple page-by-page pipeline:

1. **PDF text extraction**
   `PDFExtractor` uses PyMuPDF to extract text from each page of the PDF.

2. **OCR fallback**
   If a page has very little extracted text, the system assumes it may be scanned or image-based and runs OCR using PaddleOCR.

3. **Text cleaning**
   The extracted text is cleaned while preserving line breaks. Preserving lines is important because section headings are usually line-based.

4. **Heading detection**
   `HeadingDetector` checks the top lines of each page for heading-like patterns such as:

   - `Form 1`
   - `Form No. 2`
   - `Annexure A`
   - `Appendix B`

   It also supports cases where the title is on the next line:

   ```text
   FORM 1
   Bid Submission Form
   ```

5. **Section classification**
   `SectionClassifier` classifies detected headings as `Form` or `Annexure`, extracts the identifier, and separates the display name from the title.

6. **Page range detection**
   `PageRangeDetector` treats each detected heading as the start of a new section. A section ends one page before the next detected section. The last section ends on the final PDF page.

7. **JSON formatting**
   `formatter.py` converts the final section list into the expected JSON output format.

## Tools & Models Used

- **Python**: main implementation language
- **PyMuPDF / fitz**: text extraction from digital PDFs
- **PaddleOCR**: OCR fallback for scanned/image-based PDF pages
- **OpenCV**: image handling support for OCR
- **NumPy**: converting PDF page pixmaps into arrays for OCR
- **Regex-based heuristics**: heading detection and classification

No LLM is used in the current parsing pipeline. The solution is deterministic and rule-based.

## Trade-offs and Assumptions

- The parser assumes Forms and Annexures usually begin with clear headings like `Form 1` or `Annexure A`.
- It assumes the section heading appears near the top of the first page of that section.
- Page ranges are inferred from detected section starts, not from a table of contents.
- Output page numbers are based on PDF page index, not necessarily the printed page number inside the document.
- Regex heuristics are fast, transparent, and easy to debug, but less flexible than a trained layout-aware model.
- OCR is only used as a fallback because it is slower than direct PDF text extraction.

## Challenges Faced

- Tender PDFs can vary a lot in formatting, naming, spacing, and page layout.
- Some PDFs are text-based, while others are scanned images and require OCR.
- Section titles may be on the same line as the section name or on the next line.
- Table of contents pages can mention Forms and Annexures before the actual sections begin.
- Repeated headers across multiple pages can look similar to new section starts.
- OCR can misread characters such as `O` vs `0`, `I` vs `1`, or split headings across lines.

## Handling Edge Cases

The current solution handles these cases:

- **Same-line headings**

  ```text
  Annexure A: Technical Specifications
  ```

- **Two-line headings**

  ```text
  FORM 1
  Bid Submission Form
  ```

- **Basic numbering variations**

  ```text
  Form 1
  Form No. 1
  Form IV
  Annexure A
  Appendix B
  ```

- **Scanned pages**
  If normal PDF text extraction returns too little text, OCR is used as a fallback.

- **Duplicate repeated headings**
  If the same section heading repeats on consecutive pages, the range detector avoids creating duplicate entries for the exact same section.

- **Single-page sections**
  If a section starts and ends on the same page, the JSON output uses a single page value such as `"9"`.

## Known Limitations

- It may detect Forms/Annexures listed in the table of contents as real section starts.
- It may miss sections that begin in the middle or bottom of a page.
- It may miss unusual labels such as `Attachment A`, `Schedule I(a)`, or heavily stylized headings.
- It does not understand nested hierarchy, such as Forms inside an Annexure.
- It does not use visual layout signals like font size, bold text, or bounding boxes yet.
- OCR quality directly affects detection accuracy for scanned PDFs.

## Possible Improvements

- Add table-of-contents detection and skip TOC entries.
- Use PyMuPDF blocks/spans to detect larger or bold heading text.
- Add fuzzy matching for OCR mistakes like `F0RM` instead of `FORM`.
- Support more naming patterns such as `Schedule`, `Attachment`, and `Enclosure`.
- Add unit tests with sample page text for common tender formats.
- Export both JSON and human-readable text formats through a command-line flag.
