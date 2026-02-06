from explainer.code_parser import CodeParser


def test_parse_python_file(tmp_path):
    # Crear un archivo temporal de prueba
    content = """
def hello(name):
    return f"Hello {name}"

class Greeter:
    def __init__(self):
        pass
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(content)

    parser = CodeParser()
    result = parser.parse_file(str(file_path))

    assert result["language"] == "python"
    assert result["file_name"] == "test.py"
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "hello"
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Greeter"


def test_parse_generic_file(tmp_path):
    content = "console.log('hello');"
    file_path = tmp_path / "test.js"
    file_path.write_text(content)

    parser = CodeParser()
    result = parser.parse_file(str(file_path))

    assert result["language"] == "generic"
    assert result["total_lines"] == 1
