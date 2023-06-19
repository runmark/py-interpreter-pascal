INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    "INTEGER",
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
    "EOF",
)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Lexer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]


class Interpreter:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        pass
