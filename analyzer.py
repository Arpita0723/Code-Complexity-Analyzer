import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = 0
        self.loops = 0
        self.ifs = 0
        self.recursive_functions = set()
        self.current_function = None
        self.current_depth = 0
        self.max_depth = 0
    
    def increase_depth(self,node):
        self.current_depth +=1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -=1
    
    def visit_FunctionDef(self, node):
        self.functions += 1
        prev_function = self.current_function  # Save previous (in case of nested defs)
        self.current_function = node.name
        self.increase_depth(node)
        self.generic_visit(node)  # Visit body of function
        self.current_function = prev_function  # Restore previous

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == self.current_function:
                self.recursive_functions.add(self.current_function)
        self.generic_visit(node)

    def visit_For(self, node):
        self.loops += 1
        self.increase_depth(node)

    def visit_While(self, node):
        self.loops += 1
        self.increase_depth(node)

    def visit_If(self, node):
        self.ifs += 1
        self.increase_depth(node)
