# processing/heading_detector.py

import re


class HeadingDetector:

    def __init__(self):
        self.section_pattern = re.compile(
            r"^\s*(?:\d+(?:\.\d+)*[\).]?\s*)?("
            r"form\s*(?:no\.?|number)?\s*[-.:]?\s*[0-9ivxlcdm]+"
            r"|annex(?:ure)?\s*[-.:]?\s*[a-z0-9]+"
            r"|appendix\s*[-.:]?\s*[a-z0-9]+"
            r")\b",
            re.IGNORECASE
        )

        self.noise_pattern = re.compile(
            r"\b(table of contents|index|checklist|list of forms|page\s+\d+)\b",
            re.IGNORECASE
        )

    def detect_heading(self, text):

        lines = text.split("\n")

        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            return None

        top_lines = lines[:8]

        for index, line in enumerate(top_lines):
            if self.noise_pattern.search(line):
                continue

            match = self.section_pattern.search(line)

            if not match:
                continue

            heading = line

            if self._looks_incomplete_heading(line) and index + 1 < len(top_lines):
                next_line = top_lines[index + 1]

                if not self.noise_pattern.search(next_line):
                    heading = f"{line} {next_line}"

            return self._normalize_heading(heading)

        return None

    def _looks_incomplete_heading(self, line):
        line = line.strip()

        return bool(re.fullmatch(self.section_pattern, line.rstrip(":-. ")))

    def _normalize_heading(self, heading):
        heading = re.sub(r"\s+", " ", heading)
        heading = re.sub(r"^\d+(?:\.\d+)*[\).]?\s*", "", heading)
        heading = heading.strip(" :-\u2013")

        return heading
