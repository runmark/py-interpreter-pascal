# TOKEN TYPES
INTEGER, PLUS, MINUS, MULTIPLY, DIVID, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVID",
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
        operator_stack = []
        operand_stack = []

        # set current token to the first token taken from input
        self._current_token = self.get_next_token()

        while self._current_token.value != None:
            token = self._current_token
            if token.type in (INTEGER):
                operand_stack.append(token)
                self.eat(INTEGER)
            elif token.type in (PLUS, MINUS, MULTIPLY, DIVID):
                operator_stack.append(token)
                self.eat(token.type)
            else:
                self.error()
        # after the above call the self._current_token is set to EOF token

        result = 0
        # expr above token op
        while len(operator_stack) > 0:
            left = operand_stack.pop(-1)
            right = operand_stack.pop(-1)
            op = operator_stack.pop(-1)
            if op.type == PLUS:
                result = left.value + right.value
            elif op.type == MINUS:
                result = left.value - right.value
            operand_stack.append(Token(INTEGER, result))
        return operand_stack.pop().value
