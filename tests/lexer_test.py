import string

from pyacc import TokenType, Lexer


def test_json():
    control_characters = ''.join([chr(i) for i in range(32)])
    control_characters += chr(127)

    json_true = TokenType("json true", "true")

    json_false = TokenType("json false", "false")

    json_null = TokenType("json null", "null")

    json_open_sq_bracket = TokenType("json open sq bracket", "\[")

    json_close_sq_bracket = TokenType("json close sq bracket", "]")

    json_open_curly_bracket = TokenType("json open curly bracket", "{")

    json_close_curly_bracket = TokenType("json close curly bracket", "}")

    json_comma = TokenType("json comma", ",")

    hex_4 = "[{0}]".format(string.hexdigits) * 4
    json_string = TokenType("json string", r'"([^"\\{0}]|\\(["\\/bfnrt]|u{1}))*"'.format(control_characters, hex_4))

    json_number = TokenType("json number", "-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")

    tokens = [
        json_true,
        json_false,
        json_null,
        json_open_sq_bracket,
        json_close_sq_bracket,
        json_open_curly_bracket,
        json_close_curly_bracket,
        json_comma,
        json_string,
        json_number,
    ]
    skip_chars = [
        " ",
        "\r",
        "\n",
        "\t",
    ]
    lexer = Lexer(tokens, skip_chars)

    tokens = lexer.lex(r'["hdyuik", "\u20AC\uDd1E", "宇"]')
    token_types = [token.token_type for token in tokens]
    expect = [
        json_open_sq_bracket,
        json_string,
        json_comma,
        json_string,
        json_comma,
        json_string,
        json_close_sq_bracket,
    ]
    assert token_types == expect


    tokens = lexer.lex(r'{}, true false null -123.7e+05')
    token_types = [token.token_type for token in tokens]
    expect = [
            json_open_curly_bracket,
            json_close_curly_bracket,
            json_comma,
            json_true,
            json_false,
            json_null,
            json_number,
        ]
    assert token_types == expect

def test():
    test_json()

test()
