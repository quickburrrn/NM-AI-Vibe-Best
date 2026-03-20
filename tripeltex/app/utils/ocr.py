from pathlib import Path


async def extract_text_from_file(file_obj) -> str:
    """Best-effort text extraction placeholder used by the parser."""
    if file_obj is None:
        return ""

    if isinstance(file_obj, bytes):
        return file_obj.decode("utf-8", errors="ignore")

    if isinstance(file_obj, str):
        path = Path(file_obj)
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8", errors="ignore")
        return file_obj

    filename = getattr(file_obj, "filename", None)
    if filename:
        return filename

    return str(file_obj)
