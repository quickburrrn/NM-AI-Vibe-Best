from pathlib import Path

from app.utils.ocr import extract_text_from_file


def test_extract_text_from_path(tmp_path: Path):
    sample_file = tmp_path / "invoice.txt"
    sample_file.write_text("hello from file", encoding="utf-8")

    result = __import__("asyncio").run(extract_text_from_file(str(sample_file)))

    assert result == "hello from file"


def test_extract_text_from_bytes():
    result = __import__("asyncio").run(extract_text_from_file(b"invoice-bytes"))

    assert result == "invoice-bytes"
