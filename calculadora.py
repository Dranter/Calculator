# Calculadora logica
import ast
import operator
import math

OPERACIONES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow, # exponente
    ast.USub: operator.neg # negacion (-5)
}

# pasamos de grados a radianes para sin/cos/tan
FUNCIONES = {
    # Trigonometria
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "sqrt": math.sqrt,  # raiz cuadrada
    "log": math.log10,  # log en base 10
    "ln": math.log,     # log natural
    "abs": abs,          # num absoluto
    # Conversion numerica
    "bin": lambda x: bin(int(x)),
    "oct": lambda x: oct(int(x)),
    "hex": lambda x: hex(int(x)),
    "dec": lambda x: int(x) # si x ya es numero
}

CONSTANTES = {
    "pi": math.pi,
    "e": math.e
}

def evaluar_expresion(expr: str):
    # Parsear la expresion como un arbol
    # eval para una unica expresion como 3+4*2
    # exec para bloques completos de codigo como multiples lineas, 
    # definiciones de funciones...
    # single para fragmentos interactivos (modo consola)
    tree = ast.parse(expr, mode='eval')
    return _evaluar(tree.body)

def _evaluar(node):
    if isinstance(node, ast.BinOp): # Operacion binaria: 3 + 4, 5 * 2...
        left = _evaluar(node.left)
        right = _evaluar(node.right)
        op = OPERACIONES[type(node.op)]
        return op(left, right)
    
    elif isinstance(node, ast.UnaryOp): # para los negativos
        operand = _evaluar(node.operand)
        op = OPERACIONES[type(node.op)]
        return op(operand)
    
    elif isinstance(node, ast.Constant): # numeros literales
        return node.value
    
    elif isinstance(node, ast.Call): # para FUNCIONES
        func_name = node.func.id # nombre de la funcion llamada
        if func_name not in FUNCIONES: # si no esta en FUNCIONES...
            raise ValueError(f"Funcion no permitida: {func_name}")
        args = [_evaluar(arg) for arg in node.args]
        return FUNCIONES[func_name](*args)
    
    elif isinstance(node, ast.Name): # si no esta en CONSTANTES...
        name = node.id
        if name in CONSTANTES:
            return CONSTANTES[name]
        else:
            raise ValueError(f"Nombre no permitido: {name}")
        
    else:
        raise ValueError(f"Nodo no permitido: {type(node)}")
