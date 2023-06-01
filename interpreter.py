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
        self._current_token = None
        self._pos = 0

    def error(self):
        raise Exception("Error parsing input")

    def get_next_token(self) -> Token:
        text = self._text

        # verify that the pos is within a legal range
        if self._pos >= len(text):
            return Token(EOF, None)

        # move pos forward and get the pos-th char
        curr_char = self._text[self._pos]
        token_chars = ""

        # move the pos forward until the char that the pos points to is not digit
        while curr_char.isdigit():
            token_chars += curr_char
            self._pos += 1
            if self._pos < len(text):
                curr_char = self._text[self._pos]
            else:
                break

        # depend on the got char infer its token type
        if token_chars:
            return Token(INTEGER, int(token_chars))

        if curr_char == "+":
            token = Token(PLUS, curr_char)
            self._pos += 1
            return token

        if curr_char == "-":
            token = Token(MINUS, curr_char)
            self._pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # get next token and verify the type is compliant with token_type
        if self._current_token.type == token_type:
            self._current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr text -> INTEGER PLUS INTEGER"""

        # set current token to the first token taken from input
        self._current_token = self.get_next_token()

        # verify the token to be a single digit integer and forward
        left = self._current_token
        self.eat(INTEGER)

        # verify the token to be a '+' token and forward
        op = self._current_token
        self.eat(PLUS)

        # verify the token to be a single digit integer and forward
        right = self._current_token
        self.eat(INTEGER)

        # expr above token op
        result = left.value + right.value
        return result
