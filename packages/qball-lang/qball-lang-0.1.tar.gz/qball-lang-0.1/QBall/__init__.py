import QBall.lexer
import QBall.interpreter


def evaluate(qballcode: str):
    try:
        if qballcode[:4] == "run ":
            command = open(f"{qballcode[4:]}.qball").read()
        try:
            result = lexer.lexer(command).generate_tokens()
        except NameError:
            result = lexer.lexer(qballcode).generate_tokens()
        interpret = interpreter.interpreter(result)
        pos = interpret.pos
        interpret.interpret()
    except Exception as e:
        try:
            print(f"\033[91mError at line {pos.line} starting at char {pos.char}: {e}\033[00m")
        except NameError:
            print(f"\033[91mLexer error: {e}\033[00m")
