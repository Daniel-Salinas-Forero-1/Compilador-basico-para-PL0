from graphviz import Digraph
from Nodes import *
from Visitor import Visitor


class Dot(Visitor):
    def __init__(self):
        self.dot = Digraph(comment='AST')
        self.dot.attr('node', shape='box', style='filled', color='lightgrey')
        self.dot.attr('edge', arrowhead='none')
        self.counter = 0

    def visit(self, node):
        # Redirecciona a los métodos específicos basado en el tipo del nodo
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Método genérico para nodos no específicos
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Program(self, node: Program):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'Program')
        for func in node.functions:
            func_id = func.accept(self)
            self.dot.edge(node_id, func_id)
        return node_id

    def visit_Function(self, node: Function):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'Function: {node.name}')
        for param in node.parameters:
            param_id = param.accept(self)
            self.dot.edge(node_id, param_id)
        for var in node.var_declarations:
            var_id = var.accept(self)
            self.dot.edge(node_id, var_id)
        for stmt in node.statements:
            stmt_id = stmt.accept(self)
            self.dot.edge(node_id, stmt_id)
        return node_id

    def visit_Parameter(self, node: Parameter):
        node_id = self._get_unique_id()
        self.dot.node(
            node_id, f'Parameter: {node.param_name}, Type: {node.param_type}')
        return node_id

    def visit_IfStatement(self, node: IfStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'IfStatement')

        # Procesar la condición
        condition_id = node.condition.accept(self)
        self.dot.edge(node_id, condition_id, label='condition')

        # Procesar el bloque then
        then_id = self._process_block(node.then_block)
        self.dot.edge(node_id, then_id, label='then')

        # Procesar el bloque else, si existe
        if node.else_block:
            else_id = self._process_block(node.else_block)
            self.dot.edge(node_id, else_id, label='else')

        return node_id

    def _process_block(self, block):
        if isinstance(block, list):
            # Si es una lista, procesar cada elemento
            block_id = self._get_unique_id()
            self.dot.node(block_id, 'Block')
            for stmt in block:
                stmt_id = stmt.accept(self)
                self.dot.edge(block_id, stmt_id)
            return block_id
        else:
            # Si no es una lista, procesar el nodo directamente
            return block.accept(self)

    def visit_RelationalExpression(self, node: RelationalExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'RelationalExpression: {node.operator}')
        left_id = node.left.accept(self)
        right_id = node.right.accept(self)
        self.dot.edge(node_id, left_id, label='left')
        self.dot.edge(node_id, right_id, label='right')
        return node_id

    def visit_WhileStatement(self, node: WhileStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'WhileStatement')
        condition_id = node.condition.accept(self)
        self.dot.edge(node_id, condition_id, label='condition')

        block_id = self._get_unique_id()
        self.dot.node(block_id, 'Block')
        self.dot.edge(node_id, block_id, label='block')
        for stmt in node.block:
            stmt_id = stmt.accept(self)
            self.dot.edge(block_id, stmt_id)

        return node_id

    def visit_AssignmentStatement(self, node: AssignmentStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'AssignmentStatement')

        # Procesa el lado izquierdo de la asignación
        left_id = node.left.accept(self)
        self.dot.edge(node_id, left_id)

        # Procesa el lado derecho de la asignación
        right_id = node.right.accept(self)
        self.dot.edge(node_id, right_id)

        return node_id

    def visit_ReadStatement(self, node: ReadStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'ReadStatement')
        location_id = node.location.accept(self)
        self.dot.edge(node_id, location_id, label='location')
        return node_id

    def visit_WriteStatement(self, node: WriteStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'WriteStatement')

        # Procesar la expresión
        expr_id = node.expression.accept(self)
        self.dot.edge(node_id, expr_id)

        return node_id

    def visit_ReturnStatement(self, node: ReturnStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'ReturnStatement')
        expr_id = node.expr.accept(self)
        self.dot.edge(node_id, expr_id, label='expr')
        return node_id

    def visit_BlockStatement(self, node: BlockStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'BlockStatement')
        for stmt in node.statements:
            stmt_id = stmt.accept(self)
            self.dot.edge(node_id, stmt_id)
        return node_id

    def visit_VariableExpression(self, node: VariableExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'VariableExpression: {node.variable_name}')
        return node_id

    def visit_ArrayAccessExpression(self, node: ArrayAccessExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'ArrayAccessExpression: {node.array_name}')
        index_id = node.index.accept(self)
        self.dot.edge(node_id, index_id, label='index')
        return node_id

    def visit_BinaryExpression(self, node: BinaryExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'BinaryExpression: {node.operator}')
        left_id = node.left.accept(self)
        right_id = node.right.accept(self)
        self.dot.edge(node_id, left_id, label='left')
        self.dot.edge(node_id, right_id, label='right')
        return node_id

    def visit_UnaryExpression(self, node: UnaryExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'UnaryExpression: {node.operator}')
        operand_id = node.operand.accept(self)
        self.dot.edge(node_id, operand_id, label='operand')
        return node_id

    def visit_LiteralExpression(self, node: LiteralExpression):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'LiteralExpression: {node.value}')
        return node_id

    def visit_FunctionCall(self, node: FunctionCall):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'FunctionCall: {node.function_name}')
        for arg in node.arguments:
            arg_id = arg.accept(self)
            self.dot.edge(node_id, arg_id)
        return node_id

    def visit_NumberLiteral(self, node: NumberLiteral):
        node_id = self._get_unique_id()
        self.dot.node(node_id, f'NumberLiteral: {node.value}')
        return node_id

    def visit_VariableExpression(self, node: VariableExpression):
        node_id = self._get_unique_id()
        # Cambiado de variable_name a var_name
        self.dot.node(node_id, f'VariableExpression: {node.var_name}')
        return node_id

    def visit_ReturnStatement(self, node: ReturnStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'ReturnStatement')
        if node.expr:
            expr_id = node.expr.accept(self)
            self.dot.edge(node_id, expr_id)
        return node_id

    def visit_PrintStatement(self, node: PrintStatement):
        node_id = self._get_unique_id()
        self.dot.node(node_id, 'PrintStatement')

        # Verifica si node.value es un nodo del AST o una cadena
        if isinstance(node.value, Node):
            value_id = node.value.accept(self)
            self.dot.edge(node_id, value_id)
        else:  # Si es una cadena, añade el valor directamente
            value_label = f'Literal: {node.value}'
            value_id = self._get_unique_id()
            self.dot.node(value_id, value_label)
            self.dot.edge(node_id, value_id)

        return node_id

    def _get_unique_id(self):
        self.counter += 1
        return f'node{self.counter}'

def render_dot(ast):
    visitor = Dot()
    ast.accept(visitor)
    return visitor.dot
