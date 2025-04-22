from lexer import tokenize
from ast_nodes import Block, Assign

class Parser:
    def __init__(self, tokens):
        if not hasattr(tokens, '__iter__'):
            raise TypeError("tokens must be an iterable")
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
            # Skip NEWLINE tokens
            while self.current_token and self.current_token[0] == 'NEWLINE':
                self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        """program -> block"""
        return self.block()

    def block(self):
        """block -> '{' stmt* '}'"""
        if self.current_token and self.current_token[0] == 'LBRACE':
            self.next_token()
            statements = []
            while self.current_token and self.current_token[0] != 'RBRACE':
                if self.current_token[0] == 'END':
                    self.next_token()
                    continue
                if self.current_token is None:
                    raise SyntaxError("Unexpected end of input")
                if self.current_token[0] == 'RBRACE':
                    break
                if self.current_token[0] == 'PRINT':
                    statements.append(self.print_stmt())
                else:   
                    statements.append(self.statement())
            if self.current_token and self.current_token[0] == 'RBRACE':
                self.next_token()
                print(statements)
                return Block(statements)
            else:
                raise SyntaxError(f"Expected '}}' at the end of block, got {self.current_token}")
        else:
            raise SyntaxError(f"Expected '{{' at the start of block, got {self.current_token}")

    def statement(self):
        """stmt -> decl | block | assign | print_stmt"""
        if self.current_token and self.current_token[0] in {'FLOAT_KW', 'INT_KW', 'STRING_KW', 'BOOL_KW'}:
            # If the token is a type keyword, it's a declaration
            return self.decl()
        elif self.current_token and self.current_token[0] == 'LBRACE':
            # If the token is '{', it's a block
            return self.block()
        
        elif self.current_token and self.current_token[0] == 'ID':
            # If the token is an identifier, it's an assignment
            return self.assign()
        elif self.current_token and self.current_token[0] == 'PRINT':
            # If the token is 'PRINT', it's a print statement
            return self.print_stmt()
        else:
            raise SyntaxError(f"Unexpected token in statement: {self.current_token}")

    def decl(self):
        """decl -> type ID '=' expr ';'"""
        type_token = self.current_token  # Capture the type (e.g., 'int', 'float')
        self.next_token()  # Consume the type token
        if self.current_token and self.current_token[0] == 'ID':
            var_name = self.current_token[1]  # Capture the variable name
            self.next_token()  # Consume the ID token
            if self.current_token and self.current_token[0] == 'ASSIGN':
                self.next_token()  # Consume the '=' token

                value = self.expr()  # Parse the expression
                if self.current_token and self.current_token[0] == 'END':
                    self.next_token()  # Consume the ';' token
                    return Assign(var_name, value)  # Return an assignment node
                else:
                    raise SyntaxError(f"Expected ';' at the end of declaration, got {self.current_token}")
            else:
                raise SyntaxError(f"Expected '=' in declaration, got {self.current_token}")
        else:
            raise SyntaxError(f"Expected variable name in declaration, got {self.current_token}")

    def assign(self):
        """assign -> ID '=' expr ';'"""
        var_name = self.current_token[1]  # Get the variable name
        self.next_token()  # Consume the ID token
        if self.current_token and self.current_token[0] == 'ASSIGN':
            self.next_token()  # Consume the '=' token
            value = self.expr()  # Parse the expression
            if self.current_token and self.current_token[0] == 'END':
                self.next_token()  # Consume the ';' token
                return Assign(var_name, value)  # Return an assignment node
            else:
                raise SyntaxError(f"Expected ';' at the end of assignment, got {self.current_token}")
        else:
            raise SyntaxError(f"Expected '=' in assignment, got {self.current_token}")

    def print_stmt(self):
        """print_stmt -> 'print' '(' expr ')' ';'"""
        self.next_token()  # Consume 'print'
        if self.current_token and self.current_token[0] == 'LPAREN':
            self.next_token()
            value = self.expr()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.next_token()
                if self.current_token and self.current_token[0] == 'END':
                    self.next_token()
                    return f"Print({value})"
                else:
                    raise SyntaxError(f"Expected ';' at the end of print statement, got {self.current_token}")
            else:
                raise SyntaxError(f"Expected ')' in print statement, got {self.current_token}")
        else:
            raise SyntaxError(f"Expected '(' in print statement, got {self.current_token}")

    def expr(self):
        """expr -> term (( '+' | '-' ) term)*"""
        node = self.term()
        while self.current_token and self.current_token[0] in {'PLUS', 'MINUS'}:
            op_token = self.current_token
            self.next_token()
            right_node = self.term()
            node = [op_token[1], node, right_node]  # Combine terms with the operator
        return node

    def term(self):
        """term -> factor (( '*' | '/' ) factor)*"""
        node = self.factor()
        while self.current_token and self.current_token[0] in {'MULTIPLY', 'DIVIDE'}:
            op_token = self.current_token
            self.next_token()
            right_node = self.factor()
            node = [op_token[1], node, right_node]  # Combine factors with the operator
        return node

    def factor(self):
        """factor -> NUMBER | INTEGER |  ID | STRING | '(' expr ')'"""
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")
        if self.current_token[0] == 'NUMBER':
            node = float(self.current_token[1]) if '.' in self.current_token[1] else int(self.current_token[1])
            self.next_token()
            return node
        elif self.current_token[0] == 'INTEGER':
            node = int(self.current_token[1])
            self.next_token()
            return node
        elif self.current_token[0] == 'FLOAT':
            node = float(self.current_token[1])
            self.next_token()
            return node
        elif self.current_token[0] == 'BOOL':
            node = self.current_token[1] == 'true'
            self.next_token()
            return node
        elif self.current_token[0] == 'ID':
            node = self.current_token[1]
            self.next_token()
            return node
        elif self.current_token[0] == 'STRING':
            node = self.current_token[1]
            self.next_token()
            return node
        elif self.current_token[0] == 'LPAREN':
            self.next_token()
            node = self.expr()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.next_token()
                return node
            else:
                raise SyntaxError(f"Expected ')' after expression, got {self.current_token}")
        else:
            raise SyntaxError(f"Unexpected token in factor: {self.current_token}")
