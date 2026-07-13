import re


def clean_text(text):
    """
    Clean extracted PDF text.
    """

    if not text:
        return ""

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove Python shell prompts
    text = re.sub(r"^>>> ?", "", text, flags=re.MULTILINE)

    # Remove long separator lines
    text = re.sub(r"[-=]{5,}", "", text)

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()