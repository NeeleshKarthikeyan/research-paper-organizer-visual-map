"""
Client for extracting usable text from local PDF files.
"""

import os
import logging
from typing import Optional
from pypdf import PdfReader
from src.schemas import PaperInput

logger = logging.getLogger(__name__)


def extract_text_from_pdf(filepath: str) -> Optional[str]:
    """Extract text from a local PDF path safely."""
    if not os.path.exists(filepath):
        logger.error(f"PDF file not found: {filepath}")
        return None
    
    if not filepath.lower().endswith('.pdf'):
        logger.error(f"File is not a PDF: {filepath}")
        return None

    try:
        reader = PdfReader(filepath)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        full_text = "\n".join(text_parts).strip()
        
        if not full_text:
            logger.warning(f"No extractable text found in PDF: {filepath}")
            return None
            
        return full_text
    except Exception as e:
        logger.error(f"Error parsing PDF '{filepath}': {e}")
        return None


def parse_pdf_to_paper(filepath: str) -> Optional[PaperInput]:
    """Parse a PDF and convert it into a PaperInput model."""
    full_text = extract_text_from_pdf(filepath)
    
    if not full_text:
        return None
        
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    
    # We use the first 1500 characters as a rough proxy for the abstract 
    # to feed the deterministic heuristics that depend heavily on abstract length/density.
    abstract = full_text[:1500].replace("\n", " ").strip() + "..."
    
    return PaperInput(
        title=title,
        abstract=abstract,
        full_text=full_text,
        user_level="beginner",
        source="pdf",
        source_url=filepath
    )
