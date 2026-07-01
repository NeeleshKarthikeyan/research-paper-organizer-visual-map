"""
Client for querying the arXiv API and converting XML metadata into PaperInput objects.
"""

import logging
import xml.etree.ElementTree as ET
from typing import List
import requests

from src.schemas import PaperInput

ARXIV_API_URL = "https://export.arxiv.org/api/query"

logger = logging.getLogger(__name__)


def fetch_arxiv_papers(search_query: str, max_results: int = 5) -> List[PaperInput]:
    """Query arXiv API and return a list of parsed PaperInput objects.

    Handles network errors gracefully by returning an empty list without crashing.
    """
    params = {
        "search_query": f"all:{search_query}",
        "start": 0,
        "max_results": max_results,
    }

    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return parse_arxiv_xml(response.text)
    except requests.RequestException as e:
        logger.error(f"Error fetching papers from arXiv API: {e}")
        print(f"\n[Warning] Could not connect to arXiv API or request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error parsing arXiv response: {e}")
        print(f"\n[Warning] Error processing arXiv response: {e}")
        return []


def parse_arxiv_xml(xml_content: str) -> List[PaperInput]:
    """Parse arXiv Atom XML response into PaperInput models."""
    papers: List[PaperInput] = []
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    try:
        root = ET.fromstring(xml_content)
        entries = root.findall("atom:entry", namespaces)

        for entry in entries:
            title_elem = entry.find("atom:title", namespaces)
            summary_elem = entry.find("atom:summary", namespaces)
            id_elem = entry.find("atom:id", namespaces)
            published_elem = entry.find("atom:published", namespaces)

            title = (
                title_elem.text.replace("\n", " ").strip()
                if title_elem is not None and title_elem.text
                else "Untitled Paper"
            )
            abstract = (
                summary_elem.text.replace("\n", " ").strip()
                if summary_elem is not None and summary_elem.text
                else "No abstract available."
            )
            source_url = (
                id_elem.text.strip()
                if id_elem is not None and id_elem.text
                else None
            )
            published_date = (
                published_elem.text[:10]
                if published_elem is not None and published_elem.text
                else None
            )

            # Authors
            author_elems = entry.findall("atom:author", namespaces)
            authors = []
            for a_elem in author_elems:
                name_elem = a_elem.find("atom:name", namespaces)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text.strip())

            # Category
            category_elem = entry.find("arxiv:primary_category", namespaces)
            category = None
            if category_elem is not None:
                category = category_elem.attrib.get("term")
            else:
                cat_elem = entry.find("atom:category", namespaces)
                if cat_elem is not None:
                    category = cat_elem.attrib.get("term")

            paper = PaperInput(
                title=title,
                abstract=abstract,
                user_level="beginner",
                source_url=source_url,
                authors=authors if authors else None,
                published_date=published_date,
                source="arxiv",
                category=category,
            )
            papers.append(paper)

    except ET.ParseError as e:
        logger.error(f"XML parse error: {e}")

    return papers
