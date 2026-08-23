# Calculadora con ANTLR 4 utilizando el Patrón Visitor

Integrantes: Dylan Torres - Juan Gomez - Javier Rosero

---

##  Introducción y Fundamentos

Este trabajo consiste en el diseño e implementación de una calculadora aritmética interactiva basada en el Capítulo 4 (*A Quick Tour*) del libro de referencia *The Definitive ANTLR 4 Reference* de Terence Parr.

El objetivo principal es desacoplar la gramática del lenguaje de la lógica de evaluación. En lugar de incrustar acciones en código Java directamente dentro de las reglas gramaticales, ANTLR 4 genera un árbol sintáctico (Parse Tree) y proporciona el patrón de diseño **Visitor**, permitiendo recorrer el árbol y calcular los resultados de forma estructurada, modular y extensible.

---

##  Estructura del Repositorio

El proyecto mantiene una estructura organizada donde únicamente se conservan los archivos fuente, las pruebas y la documentación:

```text
Calculadora_ANTLR4/
├── LabeledExpr.g4              # Gramática de la calculadora con etiquetas en cada alternativa
├── EvalVisitor.java            # Implementación del Visitor en Java (evaluador aritmético y memoria)
├── Calc.java                   # Punto de entrada de la aplicación
├── README.md                   # Documentación técnica del proyecto
└── pruebas/                    # Casos de prueba organizados por escenario
    ├── 01_aritmetica_basica.txt
    ├── 02_precedencia_parentesis.txt
    ├── 03_variables_asignacion.txt
    ├── 04_division_por_cero.txt
    ├── 05_comando_clear.txt
    └── todas.txt
```

---

##  Instrucciones de Compilación y Ejecución

Para compilar y ejecutar el proyecto manualmente en la terminal, sitúate en la raíz del repositorio y ejecuta los siguientes comandos:

### Paso 1: Generar las clases del analizador con soporte para Visitor
```bash
antlr4 -no-listener -visitor LabeledExpr.g4
```
*Nota: La opción `-visitor` genera las interfaces y clases base necesarias para implementar el patrón Visitor, mientras que `-no-listener` omite la generación de listeners innecesarios.*

### Paso 2: Compilar el código fuente en Java
```bash
javac *.java
```

### Paso 3: Ejecutar la suite completa de pruebas
```bash
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/todas.txt
```

### Paso 4: Ejecutar pruebas por escenarios individuales
```bash
# Operaciones aritméticas básicas
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/01_aritmetica_basica.txt

# Precedencia de operadores y uso de paréntesis
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/02_precedencia_parentesis.txt

# Asignación y reutilización de variables en memoria
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/03_variables_asignacion.txt

# Manejo de división por cero y variables no inicializadas
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/04_division_por_cero.txt

# Comando clear para reiniciar la memoria
java -cp "$HOME/.local/lib/antlr-4.13.2-complete.jar:." Calc pruebas/05_comando_clear.txt
```

---

##  Diseño de la Gramática (`LabeledExpr.g4`)

La gramática utiliza etiquetas (iniciadas con `#`) al final de cada alternativa. Estas etiquetas le indican a ANTLR 4 que genere métodos de visita específicos en el Visitor para cada tipo de expresión, en lugar de un único método genérico por regla.

```antlr
grammar LabeledExpr;

// Reglas sintácticas
prog
    : stat+
    ;

stat
    : expr NEWLINE                # printExpr
    | ID '=' expr NEWLINE         # assign
    | 'clear' NEWLINE             # clear
    | NEWLINE                     # blank
    ;

expr
    : expr op=('*'|'/') expr      # MulDiv
    | expr op=('+'|'-') expr      # AddSub
    | INT                         # int
    | ID                          # id
    | '(' expr ')'                # parens
    ;

// Reglas léxicas
MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;

ID      : [a-zA-Z]+ ;
INT     : [0-9]+ ;
NEWLINE : '\r'? '\n' ;
WS      : [ \t]+ -> skip ;
```

**Aspectos clave de la gramática:**
- **Precedencia de operadores:** En ANTLR 4, las alternativas listadas primero tienen mayor precedencia. Al ubicar la regla `MulDiv` antes que `AddSub`, la multiplicación y división se evalúan automáticamente antes que la suma y la resta sin requerir reglas intermedias complejas.
- **Asociatividad:** Las operaciones son asociativas por la izquierda de forma predeterminada.
- **Etiquetas personalizadas:** Etiquetas como `# printExpr`, `# assign`, `# MulDiv`, `# AddSub` y `# parens` generan métodos independientes como `visitMulDiv()` o `visitAssign()`.

---

##  Casos de Uso y Manejo de Situaciones Especiales

### A. Operaciones Aritméticas Estándar
La calculadora soporta las operaciones fundamentales de números enteros: suma (`+`), resta (`-`), multiplicación (`*`) y división (`/`).

**Entrada:**

<img width="219" height="129" alt="image" src="https://github.com/user-attachments/assets/53003df9-09f3-4351-9f7d-cd565d7333fe" />

**Salida:**

<img width="135" height="125" alt="image" src="https://github.com/user-attachments/assets/c9c0d704-22ed-43da-901e-a9fcb707b6f0" />


### B. Precedencia y Uso de Paréntesis
El agrupamiento mediante paréntesis altera el orden de evaluación natural.

**Entrada:** 

<img width="235" height="121" alt="image" src="https://github.com/user-attachments/assets/13943513-8976-4282-8cdb-34cedc3ce281" />

**Salida:**

<img width="94" height="84" alt="image" src="https://github.com/user-attachments/assets/4124e29f-c399-4dc6-a8c4-0e6f9eb92f78" />


### C. Manejo de Variables y Memoria
La clase `EvalVisitor` contiene una estructura `Map<String, Integer> memory` que actúa como la memoria de la calculadora:

**Entrada:** 

<img width="255" height="119" alt="image" src="https://github.com/user-attachments/assets/1ed78209-c6e7-4a89-aff6-75e58ce9e0af" />


**Salida:**

<img width="228" height="125" alt="image" src="https://github.com/user-attachments/assets/2445231b-6257-4207-9327-04aa907ac214" />


### D. Caso Especial: División por Cero
En la ejecución estándar de Java, dividir un entero entre cero genera una excepción `ArithmeticException` que interrumpe abruptamente la ejecución del programa.

**Entrada:** 

<img width="183" height="105" alt="image" src="https://github.com/user-attachments/assets/2f96f51c-487c-42ab-980f-7d749ad7348b" />


**Salida:**

<img width="696" height="89" alt="image" src="https://github.com/user-attachments/assets/46736b67-4004-433c-aeb9-bbdd89ff86d7" />


### E. Comando `clear`
Permite restablecer la calculadora a su estado inicial borrando todas las variables registradas en la memoria mediante `memory.clear()`.

**Entrada:** 

<img width="172" height="130" alt="image" src="https://github.com/user-attachments/assets/deb0c0e0-87a4-499f-b94c-6f40bc635a86" />


**Salida:**

<img width="714" height="127" alt="image" src="https://github.com/user-attachments/assets/0b91b623-958f-4c57-9cce-89c44c34a25e" />

---
