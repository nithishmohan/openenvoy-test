import os
import sys
from typing import Sequence, Tuple, Generator, Set

import pygments
import pygments.token
import pygments.lexer
from pygments import lexers
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("source_code_analyser")


def white_characters() -> str:
    """
    Characters that count as white space if they are the only characters in a
    line.
    """
    return "(),:;[]{}"


TokenType = type(pygments.token.Token)


def _find_comments(tokens: Sequence[Tuple[TokenType, str]]) -> Generator[TokenType, None, None]:
    """

    :type tokens: object
    """

    """
    Converts strings after a colon (:) to comments.
    """

    is_after_colon = True
    for token_type, token_text in tokens:
        if is_after_colon and (token_type in pygments.token.String):
            token_type = pygments.token.Comment
        elif token_text == ":":
            is_after_colon = True
        elif token_type not in pygments.token.Comment:
            is_whitespace = len(token_text.rstrip(" \f\n\r\t")) == 0
            if not is_whitespace:
                is_after_colon = False
        yield token_type, token_text


def _format_tokens(tokens: Sequence[Tuple[TokenType, str]]) -> Generator[TokenType, None, None]:
    """

    :type tokens: object
    """

    """
    format tokens with new line
    """

    for _type, _text in tokens:
        newline = _text.find("\n")
        while newline != -1:
            yield _type, _text[: newline + 1]
            _text = _text[newline + 1:]
            newline = _text.find("\n")
        if _text != "":
            yield _type, _text


def analyse_line(lexer: pygments.lexer.Lexer, text: str) -> Generator[Set[str], None, None]:
    """

    :type lexer: object
    :type text: string

    """

    """
    convert single line to set of tokens
    """
    lines = set()
    tokens = _format_tokens(lexer.get_tokens(text))
    if lexer.name.lower() == "python":
        tokens = _find_comments(tokens)

    white_text = " \f\n\r\t" + white_characters()
    for token_type, token_text in tokens:
        is_comment = token_type in pygments.token.Comment and token_type not in (
            pygments.token.Comment.Preproc,
            pygments.token.Comment.PreprocFile,
        )
        if is_comment:
            lines.add("documentation")
        elif token_type in pygments.token.String:
            lines.add("string")
        else:
            if token_text.rstrip(white_text):
                lines.add("code")
        if token_text.endswith("\n"):
            yield lines
            lines = set()
    if len(lines) >= 1:
        yield lines


def get_lexer(source_path: str, text: str) -> pygments.lexer.Lexer:
    """

    :param text:
    :type source_path: object
    """

    """
    use this function to find the lexer of source code
    """
    """
    TODO
    pass the source code of each file and find the lexer using lexers library
    """

    lexer = pygments.lexers.guess_lexer_for_filename(source_path, text)
    return lexer


class SourceCodeAnalyser:

    @staticmethod
    def file(
            source_path: str,
            encoding: str = "automatic",
    ):
        """

        :type source_path: object
        """
        source_code = None
        source_size = 0
        try:
            source_size = os.path.getsize(source_path)
        except Exception:
            logger.error(f"The given location {source_path} is wrong")
            exit()

        if source_size == 0:
            logger.error(f"{source_path} is empty")
            exit()
        try:
            with open(source_path, "r", encoding=encoding) as source_file:
                source_code = source_file.read()
        except (LookupError, OSError, UnicodeError):
            logger.error(f"can not read file {source_path}")
            exit()
        lexer = get_lexer(source_path, source_code)
        result = {"language": lexer.name, "path": source_path, "code": 0, "documentation": 0, "white_space": 0,
                  "string": 0}

        for lines in analyse_line(lexer, source_code):
            actual_item = "white_space"
            ##checking each token in a line and prioritizing them
            for item in ("documentation", "string", "code"):
                if item in lines:
                    actual_item = item
            result[actual_item] += 1
        print()
        for key, val, in result.items():
            print(key, ":", val)
        print()

    @staticmethod
    def directory(self):
        """
        TODO
        1.call this function for source tree to find all files in the folder,
        2.Handle the duplicate files
        3.call function file for each files

        """


if __name__ == "__main__":
    file = sys.argv[1:][0]
    SourceCodeAnalyser().file(source_path=file, encoding="utf-8")
