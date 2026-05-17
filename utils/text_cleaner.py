# utils/text_cleaner.py

import re

def clean_text(text):

    lines = []

    for line in text.splitlines():
        line = re.sub(r'\s+', ' ', line)
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)
