import pytest
from unittest.mock import MagicMock, patch
from explainer.explainer import CodeExplainer

@patch('explainer.explainer.LLMHandler')
@patch('explainer.explainer.ExplanationCache')
def test_explainer_uses_cache(mock_cache_class, mock_llm_class, tmp_path):
    # Setup
    mock_cache = mock_cache_class.return_value
    mock_cache.get.return_value = "Explicación en caché"
    
    file_path = tmp_path / "test.py"
    file_path.write_text("print('hello')")
    
    explainer = CodeExplainer(use_cache=True)
    result = explainer.explain(str(file_path))
    
    assert result["explanation"] == "Explicación en caché"
    assert result["cached"] is True
    mock_cache.get.assert_called_once()

@patch('explainer.explainer.LLMHandler')
@patch('explainer.explainer.ExplanationCache')
def test_explainer_generates_new_explanation(mock_cache_class, mock_llm_class, tmp_path):
    # Setup
    mock_cache = mock_cache_class.return_value
    mock_cache.get.return_value = None
    
    mock_llm = mock_llm_class.return_value
    mock_llm.generate_explanation.return_value = "Nueva explicación"
    
    file_path = tmp_path / "test.py"
    file_path.write_text("print('hello')")
    
    explainer = CodeExplainer(use_cache=True)
    result = explainer.explain(str(file_path))
    
    assert result["explanation"] == "Nueva explicación"
    assert result["cached"] is False
    mock_llm.generate_explanation.assert_called_once()
    mock_cache.set.assert_called_once()
