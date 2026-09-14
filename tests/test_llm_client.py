"""
Unit tests for the optional LLM client integration.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.llm_client import analyze_paper_with_llm, is_llm_available
from src.schemas import SemanticAnalysis


@patch("src.llm_client.os.getenv")
def test_is_llm_available(mock_getenv):
    mock_getenv.return_value = "fake_key"
    assert is_llm_available() is True
    
    mock_getenv.return_value = None
    assert is_llm_available() is False


@patch("src.llm_client.is_llm_available", return_value=False)
def test_analyze_paper_returns_none_if_no_key(mock_is_available):
    result = analyze_paper_with_llm("Title", "Abstract")
    assert result is None


@patch("src.llm_client.is_llm_available", return_value=True)
@patch("google.genai.Client")
def test_analyze_paper_handles_api_failure(mock_client_class, mock_is_available):
    # Mock the client to raise an exception when generating content
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("API Timeout")
    mock_client_class.return_value = mock_client
    
    # It should catch the exception and return None without breaking
    result = analyze_paper_with_llm("Title", "Abstract")
    assert result is None


@patch("src.llm_client.is_llm_available", return_value=True)
@patch("google.genai.Client")
def test_analyze_paper_returns_structured_analysis(mock_client_class, mock_is_available):
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    # Mock a valid JSON string that Pydantic will parse
    mock_response.text = '''{
        "topics": ["Agents"],
        "prerequisites": ["Python"],
        "mathematical_concepts": [],
        "ml_concepts": ["LLMs"],
        "systems_concepts": [],
        "evidence": "Paper discusses LLMs.",
        "estimated_complexity": "intermediate"
    }'''
    
    mock_client.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client
    
    result = analyze_paper_with_llm("Agents and LLMs", "We discuss tool use.")
    
    assert isinstance(result, SemanticAnalysis)
    assert "Agents" in result.topics
    assert result.estimated_complexity == "intermediate"
