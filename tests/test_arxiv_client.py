"""
Unit tests for arXiv XML parser using mocked XML payload.
"""

from src.arxiv_client import parse_arxiv_xml

MOCK_ARXIV_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2303.00001v1</id>
    <published>2023-03-01T12:00:00Z</published>
    <title>Mock Transformer Agent Paper</title>
    <summary>This is a mocked abstract describing modern transformer agents.</summary>
    <author>
      <name>Alice Author</name>
    </author>
    <arxiv:primary_category term="cs.CL"/>
  </entry>
</feed>
"""


def test_parse_arxiv_xml_mock():
    papers = parse_arxiv_xml(MOCK_ARXIV_XML)
    assert len(papers) == 1
    paper = papers[0]
    assert paper.title == "Mock Transformer Agent Paper"
    assert "mocked abstract" in paper.abstract
    assert paper.source_url == "http://arxiv.org/abs/2303.00001v1"
    assert paper.authors == ["Alice Author"]
    assert paper.category == "cs.CL"
    assert paper.source == "arxiv"
