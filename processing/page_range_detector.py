# processing/page_range_detector.py

class PageRangeDetector:

    def __init__(self):
        self.sections = []

    def add_section(self, section):
        if self.sections and self._same_section(self.sections[-1], section):
            return

        # close previous section
        if self.sections:
            self.sections[-1]["end_page"] = section["start_page"] - 1

        self.sections.append(section)

    def finalize(self, total_pages):

        if self.sections:
            self.sections[-1]["end_page"] = total_pages

        return self.sections

    def _same_section(self, previous, current):
        return (
            previous.get("type") == current.get("type")
            and previous.get("identifier") == current.get("identifier")
            and self._normalize(previous.get("title")) == self._normalize(current.get("title"))
        )

    def _normalize(self, value):
        return " ".join((value or "").lower().split())
