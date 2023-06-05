# TOKEN TYPES
INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Interpreter:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_token = None
        self._current_char = self._text[self._pos]

    def error(self):
        raise Exception("Error parsing input")

    def advance(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None  # indicate end of input
        else:
            self._current_char = self._text[self._pos]

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def integer(self):
        "Return a (multidigit) integer consumed from the input."
        result = ""
        while self._current_char is not None and self._current_char.isdigit():
            result += self._current_char
            self.advance()
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
                return Token(INTEGER, self.integer())
            if self._current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self._current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            self.error()
        return Token(EOF, None)

    def eat(self, token_type):
        # get next token and verify the type is compliant with token_type
        if self._current_token.type == token_type:
            self._current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """Parser / Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """

        # set current token to the first token taken from input
        self._current_token = self.get_next_token()

        # verify the current token to be an integer
        left = self._current_token
        self.eat(INTEGER)

        # verify the current token to either a '+' or '-'
        op = self._current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        else:
            self.error()

        # verify the token to be an integer
        right = self._current_token
        self.eat(INTEGER)
        # after the above call the self._current_token is set to EOF token

        # expr above token op
        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        return result
