import java.util.HashMap;
import java.util.Map;

public class EvalVisitor extends LabeledExprBaseVisitor<Integer> {

    // Memoria para almacenar pares de variable/valor
    private final Map<String, Integer> memory = new HashMap<>();

    // Asignacion: ID '=' expr NEWLINE
    @Override
    public Integer visitAssign(LabeledExprParser.AssignContext ctx) {
        String id = ctx.ID().getText();
        Integer value = visit(ctx.expr());
        if (value != null) {
            memory.put(id, value);
            System.out.println(id + " = " + value);
        }
        return value;
    }

    // Impresion de expresion evaluada: expr NEWLINE
    @Override
    public Integer visitPrintExpr(LabeledExprParser.PrintExprContext ctx) {
        Integer value = visit(ctx.expr());
        if (value != null) {
            System.out.println(value);
        }
        return value;
    }

    // Comando para limpiar la memoria de variables: 'clear' NEWLINE
    @Override
    public Integer visitClear(LabeledExprParser.ClearContext ctx) {
        memory.clear();
        System.out.println("Memoria de variables reiniciada.");
        return 0;
    }

    // Linea en blanco: NEWLINE
    @Override
    public Integer visitBlank(LabeledExprParser.BlankContext ctx) {
        return 0;
    }

    // Numero entero: INT
    @Override
    public Integer visitInt(LabeledExprParser.IntContext ctx) {
        return Integer.valueOf(ctx.INT().getText());
    }

    // Variable: ID
    @Override
    public Integer visitId(LabeledExprParser.IdContext ctx) {
        String id = ctx.ID().getText();
        if (memory.containsKey(id)) {
            return memory.get(id);
        }
        System.err.println("Error semantico: La variable '" + id + "' no ha sido inicializada. Se asume valor 0.");
        return 0;
    }

    // Multiplicacion y Division: expr op=('*'|'/') expr
    @Override
    public Integer visitMulDiv(LabeledExprParser.MulDivContext ctx) {
        Integer left = visit(ctx.expr(0));
        Integer right = visit(ctx.expr(1));

        if (left == null || right == null) {
            return null;
        }

        if (ctx.op.getType() == LabeledExprParser.MUL) {
            return left * right;
        } else {
            // Manejo controlado de division por cero
            if (right == 0) {
                System.err.println("Error semantico: Division por cero en la expresion '" + ctx.getText() + "'.");
                return null;
            }
            return left / right;
        }
    }

    // Suma y Resta: expr op=('+'|'-') expr
    @Override
    public Integer visitAddSub(LabeledExprParser.AddSubContext ctx) {
        Integer left = visit(ctx.expr(0));
        Integer right = visit(ctx.expr(1));

        if (left == null || right == null) {
            return null;
        }

        if (ctx.op.getType() == LabeledExprParser.ADD) {
            return left + right;
        } else {
            return left - right;
        }
    }

    // Expresiones agrupadas entre parentesis: '(' expr ')'
    @Override
    public Integer visitParens(LabeledExprParser.ParensContext ctx) {
        return visit(ctx.expr());
    }
}
