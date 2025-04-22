import re

TOKEN_SPEC = [
    ('FLOAT',    r'\d+\.\d+'),    # Float literals
    ('INTEGER',  r'\d+'),         # Integer literals
    ('STRING',   r'\".*?\"'),     # String literals (double-quoted)
    ('INT_KW',      r'\bint\b'),     # Keyword: int
    ('FLOAT_KW', r'\bfloat\b'),   # Keyword: float
    ('BOOL_KW',     r'\bbool\b'),    # Keyword: bool
    ('STRING_KW', r'\bstring\b'), # Keyword: string
    ('PRINT',    r'\bprint\b'),   # Keyword: print
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('ASSIGN',   r'='),           # Assignment operator
    ('PLUS',     r'\+'),          # Addition operator
    ('MULTIPLY', r'\*'),          # Multiplication operator
    ('DIVIDE',   r'/'),           # Division operator
    ('LPAREN',   r'\('),          # Left parenthesis
    ('RPAREN',   r'\)'),          # Right parenthesis
    ('LBRACE',   r'\{'),          # Left brace
    ('RBRACE',   r'\}'),          # Right brace
    ('COMMENT',  r'#.*'),         # Single line comment
    ('SKIP',     r'[ \t]+'),      # Skip over spaces and tabs
    ('END',      r';'),           # End of statement
    ('NEWLINE',  r'\n'),          # Line endings
    ('MISMATCH', r'.'),           # Any other character
]

def tokenize(code):
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value} unexpected on line {mo.start()}')
        yield kind, value