from interpreter import Interpreter, Lexer


def main():
    while True:
        try:
            text = input("cal> ")
        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
