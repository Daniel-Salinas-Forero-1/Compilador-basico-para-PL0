import sly
import re


class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        FUN, BEGIN, END, PRINT, WRITE, READ, WHILE, BREAK, IF, THEN, ELSE, RETURN, SKIP,
        INT, FLOAT, LT, LE, GT, GE, EQ, NE, AND, OR, NOT, DO,

        # Literales
        INUMBER, FNUMBER, STRING,

        # Identificadores y Operadores
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, COMMA, SEMICOLON, LBRACKET, RBRACKET, IDENT, COLON
    }

    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'(/\*([^*]|\*[^/])*\*/)|(//.*)'

    literals = {'+', '-', '*', '/', '=', ',', ';', '(', ')', '[', ']'}

    # Palabras reservadas
    FUN = r'\bfun\b|\bFUN\b'
    BEGIN = r'\bbegin\b|\bBEGIN\b'
    END = r'\bend\b|\bEND\b'
    PRINT = r'\bprint\b|\bPRINT\b'
    WRITE = r'\bwrite\b|\bWRITE\b'
    READ = r'\bread\b|READ\b'
    WHILE = r'\bwhile\b|\bWHILE\b'
    BREAK = r'\bbreak\b|\bBREAK\b'
    IF = r'\bif\b|IF\b'
    THEN = r'\bthen\b|\bTHEN\b'
    ELSE = r'\belse|\bELSE\b'
    RETURN = r'\breturn\b|\bRETURN\b'
    SKIP = r'\bskip\b|\bSKIP\b'
    INT = r'\bint\b|\bINT\b'
    FLOAT = r'\bfloat\b|\bFLOAT\b'
    DO = r'\bdo\b|\bDO\b'

    # Operadores y símbolos
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r':='
    COLON = r':'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    SEMICOLON = r';'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LE = r'<='  # Operador menor o igual que
    GE = r'>='  # Operador mayor o igual que
    LT = r'<'  # Operador menor que
    GT = r'>'  # Operador mayor que
    EQ = r'=='  # Operador igual que

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Literales numéricos y cadenas
    @_(r'\d+\.\d*')
    def FNUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INUMBER(self, t):
        t.value = int(t.value)
        return t

    STRING = r'"([^"]*)"'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Caracter ilegal '{t.value[0]}' en la línea {self.lineno}")
        self.index += 1
