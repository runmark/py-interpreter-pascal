from interpreter import Interpreter, Lexer


class TestInterpreter:
    def test_expr(self):
        text = "3 * 2 + 5 + 7 / 3"
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        assert result == 13
