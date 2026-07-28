A safe, extensible scientific calculator built in Python, available both as a console app and as a desktop GUI. Built as a learning project to explore safe expression parsing (via Python's ast module) instead of relying on eval().

.

About the project

Most simple calculators reach for Python's eval() to parse expressions, which is a security risk since it can execute arbitrary code. This project instead parses expressions into an Abstract Syntax Tree (AST) and walks the tree manually, only allowing a whitelisted set of operations, functions, and constants. This makes it safe to evaluate user-provided math expressions without exposing the interpreter.

.

Features
Basic arithmetic: addition, subtraction, multiplication, division, exponentiation
Trigonometric functions: sin, cos, tan (input in degrees)
Other math functions: sqrt, log (base 10), ln (natural log), abs
Constants: pi, e
Number base conversion: decimal, binary (bin), octal (oct), hexadecimal (hex)

.

Two interfaces:
A console-based REPL (main.py)
A graphical desktop app built with customtkinter (main_gui.py), including a playful "kawaii mode" theme toggle

.

Tech stack
Python
ast (standard library) - safe expression parsing
math (standard library) - mathematical functions
customtkinter - modern GUI toolkit for the desktop version
