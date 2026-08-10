import re


BOOLEAN_WORDS = {
    "AND",
    "OR",
    "NOT"
}


def highlight(text, query):

    if not text or not query:
        return text

    # Remove quotes used in phrase search
    query = query.replace('"', "")

    # Remove wildcard symbol
    query = query.replace("*", "")

    # Split query into words
    words = query.split()

    # Remove Boolean operators
    words = [
        w for w in words
        if w.upper() not in BOOLEAN_WORDS
    ]

    highlighted = text

    # Highlight each search word
    for word in sorted(words, key=len, reverse=True):

        pattern = re.compile(
            rf"\b({re.escape(word)}\w*)\b",
            re.IGNORECASE
        )

        highlighted = pattern.sub(
            r"<mark>\1</mark>",
            highlighted
        )

    return highlighted