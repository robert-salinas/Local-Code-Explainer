import pytest
from fastapi.testclient import TestClient
from api.server import app
from unittest.mock import patch

client = TestClient(app)


@patch("api.server.CodeExplainer")
def test_api_explain_success(mock_explainer_class, tmp_path):
    # Setup mock
    mock_instance = mock_explainer_class.return_value
    mock_instance.explain.return_value = {
        "analysis": {
            "file_name": "test.py",
            "language": "python",
            "total_lines": 1,
            "functions": [],
            "classes": [],
            "imports": [],
        },
        "explanation": "API Test explanation",
        "cached": False,
    }

    file_path = tmp_path / "test.py"
    file_path.write_text("print('hello')")

    response = client.post(
        "/explain", json={"path": str(file_path), "model": "mistral"}
    )

    assert response.status_code == 200
    assert response.json()["explanation"] == "API Test explanation"


def test_api_explain_file_not_found():
    response = client.post("/explain", json={"path": "non_existent.py"})
    assert response.status_code == 404


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
