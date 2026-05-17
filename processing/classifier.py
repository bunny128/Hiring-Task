# processing/classifier.py

import re

from config import FORM_KEYWORDS, ANNEXURE_KEYWORDS


class SectionClassifier:

    def __init__(self):
        self.form_pattern = re.compile(
            r"^\s*form\s*(?:no\.?|number)?\s*[-.:]?\s*(?P<identifier>[0-9ivxlcdm]+)\s*[:\-\u2013.]?\s*(?P<title>.*)$",
            re.IGNORECASE
        )
        self.annexure_pattern = re.compile(
            r"^\s*(?:annexure|annex|appendix)\s*[-.:]?\s*(?P<identifier>[a-z0-9]+)\s*[:\-\u2013.]?\s*(?P<title>.*)$",
            re.IGNORECASE
        )

    def classify(self, heading):

        if not heading:
            return None

        heading_upper = heading.upper()

        for keyword in FORM_KEYWORDS:
            if keyword in heading_upper:
                return "Form"

        for keyword in ANNEXURE_KEYWORDS:
            if keyword in heading_upper:
                return "Annexure"

        return None

    def extract_section(self, heading):
        section_type = self.classify(heading)

        if not section_type:
            return None

        pattern = self.form_pattern if section_type == "Form" else self.annexure_pattern
        match = pattern.match(heading)

        if not match:
            return {
                "type": section_type,
                "identifier": None,
                "title": heading
            }

        identifier = match.group("identifier").upper()
        title = match.group("title").strip(" :-\u2013")

        return {
            "type": section_type,
            "identifier": identifier,
            "title": title or heading
        }
