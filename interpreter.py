# TOKEN TYPES
INTEGER, PLUS, MINUS, MUL, DIV, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "EOF"


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

    def _error(self):
        raise Exception("Invalid character")

    def _advance(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None  # indicate end of input
        else:
            self._current_char = self._text[self._pos]

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _integer(self):
        "Return a (multidigit) integer consumed from the input."
        result = ""
        while self._current_char is not None and self._current_char.isdigit():
            result += self._current_char
            self._advance()
        return int(result)

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self._current_char is not None:
            if self._current_char.isspace():
                self._skip_whitespace()
                continue

            if self._current_char.isdigit():
                return Token(INTEGER, self._integer())

            if self._current_char == "+":
                self._advance()
                return Token(PLUS, "+")
            if self._current_char == "-":
                self._advance()
                return Token(MINUS, "-")
            if self._current_char == "*":
                self._advance()
                return Token(MUL, "*")
            if self._current_char == "/":
                self._advance()
                return Token(DIV, "/")

            self._error()

        return Token(EOF, None)


class Interpreter:
    """Parser / Interpreter

    expr: term ((PLUS|MINUS) term)*
    term: factor ((MUL|DIV) factor)*
    factor: INTEGER
    """

    def __init__(self, lexer):
        self._lexer = lexer
        # set current token to the first token taken from the input
        self._current_token = lexer.get_next_token()

    def _error(self):
        raise Exception("Invalid syntax")

    def _eat(self, token_type):
        # get next token and verify the type is compliant with token_type
        if self._current_token.type == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self.error()

    def _factor(self):
        """Return an Integer token value.

        factor: INTEGER
        """
        token = self._current_token
        self._eat(INTEGER)
        return token.value

    def _term(self):
        result = self._factor()

        while self._current_token.type in (MUL, DIV):
            token = self._current_token
            if token.type == MUL:
                self._eat(MUL)
                result = result * self._factor()
            elif token.type == DIV:
                self._eat(DIV)
                result = result / self._factor()

        return int(result)

    def expr(self):
        result = self._term()

        while self._current_token.type in (PLUS, MINUS):
            token = self._current_token
            if token.type == PLUS:
                self._eat(PLUS)
                result = result + self._term()
            elif token.type == MINUS:
                self._eat(MINUS)
                result = result - self._term()

        return result
