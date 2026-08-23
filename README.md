# Calculadora con ANTLR 4 utilizando el Patrón Visitor

Integrantes: Dylan Torres - Juan Gomez - Javier Rosero

---

## 1. Introducción y Fundamentos

Este trabajo consiste en el diseño e implementación de una calculadora aritmética interactiva basada en el Capítulo 4 (*A Quick Tour*) del libro de referencia *The Definitive ANTLR 4 Reference* de Terence Parr.

El objetivo principal es desacoplar la gramática del lenguaje de la lógica de evaluación. En lugar de incrustar acciones en código Java directamente dentro de las reglas gramaticales, ANTLR 4 genera un árbol sintáctico (Parse Tree) y proporciona el patrón de diseño **Visitor**, permitiendo recorrer el árbol y calcular los resultados de forma estructurada, modular y extensible.

---

## 2. Estructura del Repositorio

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

## 3. Instrucciones de Compilación y Ejecución

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

## 4. Diseño de la Gramática (`LabeledExpr.g4`)

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

## 5. Casos de Uso y Manejo de Situaciones Especiales

### A. Operaciones Aritméticas Estándar
La calculadora soporta las operaciones fundamentales de números enteros: suma (`+`), resta (`-`), multiplicación (`*`) y división (`/`).

- **Entrada:** `10 + 5 * 2`
- **Comportamiento:** Se evalúa primero `5 * 2 = 10` y luego `10 + 10 = 20`.

### B. Precedencia y Uso de Paréntesis
El agrupamiento mediante paréntesis altera el orden de evaluación natural.

- **Entrada:** `(10 + 5) * 2`
- **Comportamiento:** La regla `# parens` extrae la expresión interior, evaluando primero `10 + 5 = 15` y luego `15 * 2 = 30`.

### C. Manejo de Variables y Memoria
La clase `EvalVisitor` contiene una estructura `Map<String, Integer> memory` que actúa como la memoria de la calculadora:
- Al encontrar una sentencia de asignación (`a = 15`), se evalúa la parte derecha y se almacena el valor asociado a la clave `"a"`.
- Al encontrar un identificador en una expresión posterior (`a + 5`), se busca en la memoria y se recupera su valor (`20`).
- Si una variable es utilizada sin haber sido asignada previamente, el evaluador emite un mensaje de error semántico advirtiendo que no está inicializada y utiliza `0` por defecto.

### D. Caso Especial: División por Cero
En la ejecución estándar de Java, dividir un entero entre cero genera una excepción `ArithmeticException` que interrumpe abruptamente la ejecución del programa.

En nuestra implementación, el método `visitMulDiv` valida explícitamente si el divisor (`right`) es igual a `0`:

```java
if (right == 0) {
    System.err.println("Error semantico: Division por cero en la expresion '" + ctx.getText() + "'.");
    return null;
}
```

Al detectar el divisor en cero, el programa:
1. Emite un mensaje de error descriptivo en la salida estándar de errores indicando la expresión exacta donde ocurrió el fallo.
2. Retorna `null` para propagar de forma segura el estado de error sin romper el procesamiento de las instrucciones siguientes en el archivo de entrada.

### E. Comando `clear`
Permite restablecer la calculadora a su estado inicial borrando todas las variables registradas en la memoria mediante `memory.clear()`.

---

## 6. Conclusiones

1. **Ventajas del Patrón Visitor:** Proporciona un control total sobre el recorrido del árbol sintáctico, permitiendo retornar valores directamente entre llamadas y facilitando la implementación de la lógica matemática y la gestión de memoria en código Java nativo.
2. **Separación de Responsabilidades:** La gramática únicamente describe la sintaxis formal del lenguaje, mientras que el Visitor concentra la semántica, el cálculo numérico y el control de excepciones.
3. **Robustez en la Evaluación:** El tratamiento explícito de condiciones de borde, como la división por cero y variables no definidas, garantiza una experiencia de ejecución consistente y confiable.
