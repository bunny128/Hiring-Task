# output/formatter.py

import json


def format_output(sections):
    output = []

    for section in sections:
        name = section["type"]

        if section.get("identifier"):
            name = f"{name} {section['identifier']}"

        output.append({
            "type": section["type"],
            "name": name,
            "title": section["title"],
            "pages": _format_pages(section["start_page"], section["end_page"])
        })

    return json.dumps(output, indent=2)


def _format_pages(start_page, end_page):
    if start_page == end_page:
        return str(start_page)

    return f"{start_page}-{end_page}"
