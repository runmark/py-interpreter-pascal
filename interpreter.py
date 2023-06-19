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

    def _advance(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _integer(self):
        result = ""
        while self._current_char is not None and self._current_char.isdigit():
            result += self._current_char
            self._advance()

        return int(result)

    def _error(self):
        raise Exception("Invalid character")

    def get_next_token(self):
        while self._current_char != None:
            if self._current_char.isspace():
                self._skip_whitespace()

            if self._current_char.isdigit():
                integer = self._integer()
                return Token(INTEGER, integer)

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

            if self._current_char == "(":
                self._advance()
                return Token(LPAREN, "(")

            if self._current_char == ")":
                self._advance()
                return Token(RPAREN, ")")

            self._error()

        return Token(EOF, None)


class Interpreter:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()

    def _error(self):
        raise Exception("Invalid Token")

    def _factor(self):
        token = self._current_token
        if token.type == INTEGER:
            self._eat(INTEGER)
            return token.value

        elif token.type == LPAREN:
            self._eat(LPAREN)
            result = self.expr()
            self._eat(RPAREN)
            return result

    def _term(self):
        result = self._factor()

        while self._current_token.type in (MUL, DIV):
            if self._current_token.type == MUL:
                self._eat(MUL)
                result = result * self._factor()
            elif self._current_token.type == DIV:
                self._eat(DIV)
                result = result / self._factor()

        return result

    def _eat(self, type):
        if self._current_token.type == type:
            self._current_token = self._lexer.get_next_token()
        else:
            self._error()

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        result = self._term()

        while self._current_token.type in (PLUS, MINUS):
            if self._current_token.type == PLUS:
                self._eat(PLUS)
                result = result + self._term()
            elif self._current_token.type == MINUS:
                self._eat(MINUS)
                result = result - self._term()

        return result
