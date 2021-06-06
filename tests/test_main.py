from pygments import lexers, token
from main import analyse_line


def test_can_compute_python_line_parts():
    python_lexer = lexers.get_lexer_by_name("python")

    assert list(analyse_line(python_lexer, "#")) == [set(["documentation"])]
    assert list(analyse_line(python_lexer, "s = 'x'  # x")) == [set(["documentation", "code", "string"])]


def test_can_detect_white_text():
    python_lexer = lexers.get_lexer_by_name("python")
    assert list(analyse_line(python_lexer, "{[()]};")) == [set()]


def test_can_analyze_python():
    source_lines = [
        '"Test."',
        "#!/bin/python",
        "# comment",
        "def foo():",
        '    "Write your code here"',
        '    return "foo"',
    ]
    lexer = lexers.get_lexer_by_name("python")
    source_code = "\n".join(source_lines)
    actual_line_parts = list(analyse_line(lexer, source_code))

    expected_line_parts = [{"documentation"}, {"documentation"}, {"documentation"}, {"code"}, {"documentation"},
                           {"code", "string"}]

    assert actual_line_parts == expected_line_parts
