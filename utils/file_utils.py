import os

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}

def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
