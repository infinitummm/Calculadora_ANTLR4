#!/usr/bin/make -f
# Makefile para Calculadora Científica y Graficadora ANTLR 4

ANTLR_JAR ?= $(HOME)/.local/lib/antlr-4.13.2-complete.jar
ANTLR     ?= antlr4
JAVAC     ?= javac
JAVA      ?= java
CP        := "$(ANTLR_JAR):."
GRAMMAR   := ScientificCalc.g4
MAIN      := Main

.PHONY: all generate compile run test test-all clean help

all: compile

# Generar clases del Lexer, Parser y Visitor desde la gramatica
generate:
	@echo "==> Generando código ANTLR 4..."
	$(ANTLR) -no-listener -visitor $(GRAMMAR)

# Compilar todos los archivos Java
compile: generate
	@echo "==> Compilando archivos Java..."
	$(JAVAC) -cp $(CP) *.java
	@echo "==> Compilación finalizada exitosamente."

# Ejecutar el modo interactivo por consola (REPL)
run: compile
	@echo "==> Iniciando calculadora en modo interactivo..."
	$(JAVA) -cp $(CP) $(MAIN)

# Ejecutar el archivo de pruebas oficial (ejemplos.txt)
test: compile
	@echo "==> Ejecutando ejemplos.txt..."
	$(JAVA) -cp $(CP) $(MAIN) ejemplos.txt

# Ejecutar todas las suites de prueba organizadas
test-all: compile
	@echo "==> 1. Aritmética y Reales"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/01_aritmetica_reales.txt
	@echo ""
	@echo "==> 2. Variables y Memoria"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/02_variables_memoria.txt
	@echo ""
	@echo "==> 3. Potencias y Unarios"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/03_potencia_unarios.txt
	@echo ""
	@echo "==> 4. Funciones Científicas"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/04_funciones_cientificas.txt
	@echo ""
	@echo "==> 5. Comandos clear y vars"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/05_comandos_clear_vars.txt
	@echo ""
	@echo "==> 6. Retos Extendidos"
	$(JAVA) -cp $(CP) $(MAIN) pruebas/06_retos_extendidos.txt

# Limpieza total de binarios y archivos autogenerados
clean:
	@echo "==> Limpiando archivos autogenerados y binarios..."
	@rm -f *.class *.tokens *.interp
	@rm -f ScientificCalcLexer.java ScientificCalcParser.java ScientificCalcVisitor.java ScientificCalcBaseVisitor.java
	@rm -f ScientificCalcListener.java ScientificCalcBaseListener.java
	@echo "==> Directorio limpio."

help:
	@echo "Opciones disponibles en el Makefile:"
	@echo "  make          - Genera el código ANTLR y compila todas las clases Java"
	@echo "  make compile  - Mismo comportamiento que 'make'"
	@echo "  make run      - Inicia la calculadora interactiva por consola (REPL)"
	@echo "  make test     - Ejecuta las pruebas de ejemplos.txt"
	@echo "  make test-all - Ejecuta todas las pruebas en pruebas/"
	@echo "  make clean    - Elimina todos los archivos generados y binarios .class"
