from rich import print
from Lexer import Lexer
from Parser import Parser
from Dot import render_dot

if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()

    txt = open('test.pl0').read()
    tokenized = lexer.tokenize(txt)
    ast = parser.parse(tokenized)

    print(ast)
    dot = render_dot(ast)
    print(dot)
