"""
Unit tests for the PDF parser and extraction logic.
"""

import os
import tempfile
from pypdf import PdfWriter, PdfReader
from src.pdf_parser import extract_text_from_pdf, parse_pdf_to_paper


def create_dummy_pdf(filepath: str, text_content: str):
    """Create a minimal dummy PDF for testing."""
    # pypdf's PdfWriter doesn't easily create text from scratch natively without ReportLab.
    # To keep dependencies light and self-contained, we'll just mock the extraction 
    # instead of generating a complex binary PDF manually, OR we can just write an empty PDF 
    # and mock the PdfReader.pages return value.
    
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    with open(filepath, "wb") as f:
        writer.write(f)


def test_extract_text_missing_file():
    text = extract_text_from_pdf("nonexistent_file.pdf")
    assert text is None


def test_extract_text_wrong_extension():
    with tempfile.NamedTemporaryFile(suffix=".txt") as f:
        text = extract_text_from_pdf(f.name)
        assert text is None


def test_parse_pdf_to_paper(monkeypatch):
    """Test parsing logic by mocking the underlying text extraction."""
    mock_full_text = "This is a mock abstract for a pdf paper about transformer architecture. " * 50
    
    def mock_extract(filepath):
        return mock_full_text
        
    monkeypatch.setattr("src.pdf_parser.extract_text_from_pdf", mock_extract)
    
    paper = parse_pdf_to_paper("dummy_research_paper.pdf")
    
    assert paper is not None
    assert paper.title == "dummy research paper"
    assert "transformer architecture" in paper.abstract
    assert paper.full_text == mock_full_text
    assert paper.source == "pdf"
