import sly
import Lexer
import Nodes


class Parser(sly.Parser):
    tokens = Lexer.Lexer.tokens
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    # Reglas generales y de programa
    @_("funclist")
    def program(self, p):
        return Nodes.Program(p.funclist)

    @_("funclist function")
    def funclist(self, p):
        return p.funclist + [p.function]

    @_("function")
    def funclist(self, p):
        return [p.function]

    # Definición de función y parámetros
    @_("FUN IDENT parmlist varlist BEGIN statements END")
    def function(self, p):
        return Nodes.Function(p.IDENT, p.parmlist, p.varlist, p.statements)

    @_("LPAREN parmlistitems RPAREN")
    def parmlist(self, p):
        return p.parmlistitems

    @_("LPAREN RPAREN")
    def parmlist(self, p):
        return []

    @_("parmlistitems COMMA parm")
    def parmlistitems(self, p):
        return p.parmlistitems + [p.parm]

    @_("parm")
    def parmlistitems(self, p):
        return [p.parm]

    @_("IDENT COLON typename")
    def parm(self, p):
        return Nodes.Parameter(p.IDENT, p.typename)

    # Declaraciones de variables y tipos
    @_("decllist optsemi")
    def varlist(self, p):
        return p.decllist

    @_("")
    def varlist(self, p):
        return []

    @_("decllist SEMICOLON vardecl")
    def decllist(self, p):
        return p.decllist + [p.vardecl]

    @_("vardecl")
    def decllist(self, p):
        return [p.vardecl]

    @_("parm")
    def vardecl(self, p):
        return p.parm

    @_("SEMICOLON")
    @_("")
    def optsemi(self, p):
        pass

    @_("INT")
    @_("FLOAT")
    def typename(self, p):
        return p[0].upper()

    @_("FLOAT LBRACKET expr RBRACKET", "INT LBRACKET expr RBRACKET")
    def typename(self, p):
        return Nodes.TypeName(f"{p[0].upper()}_ARRAY", p.expr)

    # Expresiones y operaciones
    @_("expr PLUS expr",
       "expr MINUS expr",
       "expr TIMES expr",
       "expr DIVIDE expr")
    def expr(self, p):
        return Nodes.BinaryExpression(p.expr0, p[1], p.expr1)

    @_("MINUS expr",
       "PLUS expr")
    def expr(self, p):
        return Nodes.UnaryExpression(p[0], p.expr)

    @_("INUMBER",
       "FNUMBER")
    def expr(self, p):
        return Nodes.NumberLiteral(p[0])

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("expr")
    def relop(self, p):
        return Nodes.Node(p.expr)

    @_("expr LT expr",
        "expr LE expr",
        "expr GT expr",
        "expr GE expr",
        "expr EQ expr",
        "expr NE expr")
    def relop(self, p):
        return Nodes.RelationalExpression(p.expr0, p[1], p.expr1)

    @_("relop AND relop",
       "relop OR relop")
    def relop(self, p):
        return Nodes.LogicalExpression(p.relop0, p[1], p.relop1)

    @_("NOT relop")
    def relop(self, p):
        return Nodes.NotExpression(p.relop)

    # Estructuras de control y declaraciones
    @_("statements SEMICOLON statement")
    def statements(self, p):
        return p.statements + [p.statement]

    @_("statement")
    def statements(self, p):
        return [p.statement]

    @_("PRINT LPAREN STRING RPAREN")
    def statement(self, p):
        return Nodes.PrintStatement(p.STRING)

    @_("IF relop THEN statement ELSE statement")
    def statement(self, p):
        # Si 'ELSE' está presente, utiliza ambos bloques 'THEN' y 'ELSE'
        return Nodes.IfStatement(p.relop, p.statement0, p.statement1)

    @_("IF relop THEN statement")
    def statement(self, p):
        # Si 'ELSE' no está presente, solo utiliza el bloque 'THEN'
        return Nodes.IfStatement(p.relop, p.statement, None)

    @_("WHILE relop DO statement")
    def statement(self, p):
        return Nodes.WhileStatement(p.relop, p.statement)

    @_("location ASSIGN expr")
    def statement(self, p):
        return Nodes.AssignmentStatement(p.location, p.expr)

    @_("READ LPAREN location RPAREN")
    def statement(self, p):
        return Nodes.ReadStatement(p.location)

    @_("WRITE LPAREN expr RPAREN")
    def statement(self, p):
        return Nodes.WriteStatement(p.expr)

    @_("RETURN expr")
    def statement(self, p):
        return Nodes.ReturnStatement(p.expr)

    @_("BREAK")
    @_("SKIP")
    def statement(self, p):
        return getattr(Nodes, f"{p[0].capitalize()}Statement")()

    @_("BEGIN statements END")
    def statement(self, p):
        return Nodes.BlockStatement(p.statements)

    # Ubicaciones y acceso a arreglos
    @_("IDENT")
    def location(self, p):
        return Nodes.VariableExpression(p.IDENT)

    @_("IDENT")
    def expr(self, p):
        return Nodes.VariableExpression(p.IDENT)

    @_("IDENT LBRACKET expr RBRACKET")
    def location(self, p):
        return Nodes.ArrayAccessExpression(p.IDENT, p.expr)

    # Operaciones compuestas
    @_("location PLUS ASSIGN expr",
       "location MINUS ASSIGN expr")
    def statement(self, p):
        return Nodes.CompoundAssignmentStatement(p.location, f"{p[1]}=", p.expr)

    # llamar funciones
    @_("IDENT LPAREN exprlist RPAREN")
    def expr(self, p):
        return Nodes.FunctionCall(p.IDENT, p.exprlist)

    @_("exprlist COMMA expr")
    def exprlist(self, p):
        return p.exprlist + [p.expr]

    @_("expr")
    def exprlist(self, p):
        return [p.expr]

    # O si necesitas manejar una lista vacía:
    @_("")
    def exprlist(self, p):
        return []

    # Manejo de errores
    def error(self, p):
        if p:
            print(p)
            print(
                f"Error de sintaxis en el token {p.value} en la línea {p.lineno}")
        else:
            print("Error de sintaxis en EOF")
