import hashlib

def generate_hash(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def clean_text(text):

    return " ".join(text.split())