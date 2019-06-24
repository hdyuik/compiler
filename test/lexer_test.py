from lexer.token import TokenType

from lexer.lexer import Lexer


def test_json():
    control_characters = ''.join([chr(i) for i in range(32)])
    control_characters += chr(127)
    json_string = TokenType("json string", r'"([^"\\{0}]|\\["\\/bfnrtu])*"'.format(control_characters))

    json_number = TokenType("json number", "-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")

    lexer = Lexer([json_string, json_number], [' '])

    tokens = lexer.lex("\"hdyuik\" 145.3e+09")
    for token in tokens:
        print(token)


def test():
    test_json()

test()
