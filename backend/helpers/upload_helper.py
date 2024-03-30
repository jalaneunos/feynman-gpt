ALLOWED_EXTENSIONS = [
    "csv", "docx", "epub", "hwp", "ipynb", "jpeg", "jpg", "mbox",
    "md", "mp3", "mp4", "pdf", "png", "ppt", "pptm", "pptx", "txt"
]

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.split(".")[1] in ALLOWED_EXTENSIONS
