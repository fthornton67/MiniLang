class Environment:
    def __init__(self):
        self.variables = {}
    def push(self):
        self.stack.append({})
    def set(self, name, value):
        self.variables[name] = value
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise RuntimeError(f"Variable '{name}' not found")
    def pop(self):
        if self.stack:
            self.variables = self.stack.pop()
        else:
            raise RuntimeError("No environment to pop")
    def __repr__(self):
        return f"Environment({self.variables})"
    def __str__(self):
        return f"Environment({self.variables})"
    
    def eval_expr(self, expr):
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            return self.get(expr)
        elif isinstance(expr, list):
            op = expr[0]
            if op == '+':
                return self.eval_expr(expr[1]) + self.eval_expr(expr[2])
            elif op == '-':
                return self.eval_expr(expr[1]) - self.eval_expr(expr[2])
            elif op == '*':
                return self.eval_expr(expr[1]) * self.eval_expr(expr[2])
            elif op == '/':
                return self.eval_expr(expr[1]) / self.eval_expr(expr[2])
        raise RuntimeError(f"Invalid expression: {expr}")