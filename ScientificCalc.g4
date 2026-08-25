grammar ScientificCalc;

// Regla inicial: Una o mas sentencias hasta el fin de archivo
prog
    : stat+ EOF
    ;

// Sentencias reconocidas
stat
    : expr NEWLINE                                               # printExpr
    | ID '=' expr NEWLINE                                        # assign
    | 'clear' NEWLINE                                            # clear
    | 'vars' NEWLINE                                             # showVars
    | 'plot' '(' expr ',' expr ',' expr ')' NEWLINE              # plotExpr
    | 'plot' '(' expr ',' expr ',' expr ',' expr ',' expr ')' NEWLINE # plotRangeExpr
    | NEWLINE                                                    # blank
    ;

// Expresiones con precedencia jerarquica
expr
    : <assoc=right> expr '^' expr                                # power
    | op=('+'|'-') expr                                          # unary
    | expr op=('*'|'/') expr                                     # mulDiv
    | expr op=('+'|'-') expr                                     # addSub
    | function '(' expr ')'                                      # functionCall
    | function2 '(' expr ',' expr ')'                            # functionCall2
    | constant                                                   # constantExpr
    | NUMBER                                                     # number
    | ID                                                         # id
    | '(' expr ')'                                               # parens
    ;

// Operadores
POW : '^' ;
MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;

// Funciones matematicas de 1 argumento
function
    : 'sin'
    | 'cos'
    | 'tan'
    | 'asin'
    | 'acos'
    | 'atan'
    | 'sqrt'
    | 'log'
    | 'ln'
    | 'abs'
    | 'exp'
    | 'floor'
    | 'ceil'
    ;

// Funciones matematicas de 2 argumentos
function2
    : 'pow'
    | 'max'
    | 'min'
    ;

// Constantes matematicas
constant
    : 'pi'
    | 'e'
    ;

// Numeros reales (enteros y decimales)
NUMBER
    : [0-9]+ ('.' [0-9]+)?
    ;

// Identificadores (variables)
ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

// Delimitador de linea
NEWLINE
    : '\r'? '\n'
    ;

// Espacios en blanco y tabulaciones ignorados
WS
    : [ \t]+ -> skip
    ;
