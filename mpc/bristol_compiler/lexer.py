import ply.lex as lex

reserved = {
  'in' : 'INPUT',
  'out': 'OUTPUT',
  'var': 'ASSIGN',
  'bit128': 'BIT128',
  'bit64': 'BIT64',
  'bit32': 'BIT32',
  'bit': 'BIT',
  'LessThan32': 'LT32',
  'Mul64Mod': 'MUL64MOD',
  'Mul64': 'MUL64',
  'Add64': 'ADD64',
  'Sub64': 'SUB64',
  'IsZero64': 'EQZ64',
  'Xor': 'XOR',
  'And':'AND',
  'Not':'NOT',
}

tokens = ['LBRACK', 'RBRACK', 'COLON', 'ID', 'EQUALS', 'LPAREN', 'RPAREN', 'COMMA', 'INPUT', 'OUTPUT', 'ASSIGN', 'LBRACE', 'RBRACE', 'NUMBER', 'BIT', 'BIT32', 'BIT64', 'BIT128', 'XOR', 'AND', 'NOT', 'LT32', 'MUL64MOD', 'MUL64', 'ADD64', 'SUB64', 'EQZ64']
t_ignore = ' \t'
t_EQUALS = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COLON = r':'
t_COMMA = r','

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'ID')    # Check for reserved words
  return t

def t_NUMBER(t):
 r'\d+'
 t.value = int(t.value)
 return t

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

lexer = lex.lex() # Build the lexer

# Test it out

# Give the lexer some input
def getTokens(f, s=None):
  if s==None:
    with open(f, "r") as f:
      lexer.input(f.read())
  else:
    lexer.input(s)
  # Tokenize
  toks = []
  while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    toks.append((tok.type,tok.value,tok.lineno))
  return toks
