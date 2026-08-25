import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ScientificEvalVisitor extends ScientificCalcBaseVisitor<Double> {

    // Tabla de simbolos para variables (nombre -> valor)
    private final Map<String, Double> memory = new HashMap<>();

    // Impresion de expresion evaluada
    @Override
    public Double visitPrintExpr(ScientificCalcParser.PrintExprContext ctx) {
        Double value = visit(ctx.expr());
        if (value != null) {
            // Formatear si es entero exacto para salida limpia
            if (value == Math.floor(value) && !Double.isInfinite(value)) {
                System.out.println(String.format("%.0f", value));
            } else {
                System.out.println(value);
            }
        }
        return value;
    }

    // Asignacion de variable: ID '=' expr
    @Override
    public Double visitAssign(ScientificCalcParser.AssignContext ctx) {
        String id = ctx.ID().getText();
        Double value = visit(ctx.expr());
        if (value != null) {
            memory.put(id, value);
            if (value == Math.floor(value) && !Double.isInfinite(value)) {
                System.out.println(id + " = " + String.format("%.0f", value));
            } else {
                System.out.println(id + " = " + value);
            }
        }
        return value;
    }

    // Comando clear: reinicia la memoria
    @Override
    public Double visitClear(ScientificCalcParser.ClearContext ctx) {
        memory.clear();
        System.out.println("Memoria eliminada.");
        return 0.0;
    }

    // Comando vars: muestra las variables en memoria
    @Override
    public Double visitShowVars(ScientificCalcParser.ShowVarsContext ctx) {
        if (memory.isEmpty()) {
            System.out.println("No hay variables definidas.");
            return 0.0;
        }
        System.out.println("--- Variables en memoria ---");
        for (Map.Entry<String, Double> entry : memory.entrySet()) {
            Double val = entry.getValue();
            if (val == Math.floor(val) && !Double.isInfinite(val)) {
                System.out.println(entry.getKey() + " = " + String.format("%.0f", val));
            } else {
                System.out.println(entry.getKey() + " = " + val);
            }
        }
        System.out.println("----------------------------");
        return 0.0;
    }

    // Comando plot(expr, xmin, xmax)
    @Override
    public Double visitPlotExpr(ScientificCalcParser.PlotExprContext ctx) {
        String exprText = ctx.expr(0).getText();
        Double xmin = visit(ctx.expr(1));
        Double xmax = visit(ctx.expr(2));

        if (xmin == null || xmax == null) {
            System.err.println("Error: Limites de graficacion invalidos.");
            return null;
        }

        if (xmin >= xmax) {
            System.err.println("Error: xmin debe ser estrictamente menor que xmax.");
            return null;
        }

        int samples = 800;
        List<Double> xs = new ArrayList<>(samples);
        List<Double> ys = new ArrayList<>(samples);

        // Guardar estado previo de x si existia
        Double previousX = memory.get("x");

        for (int i = 0; i < samples; i++) {
            double x = xmin + (double) i * (xmax - xmin) / (samples - 1);
            memory.put("x", x);
            Double y = visit(ctx.expr(0));

            if (y != null && Double.isFinite(y)) {
                xs.add(x);
                ys.add(y);
            }
        }

        // Restaurar estado previo
        if (previousX != null) {
            memory.put("x", previousX);
        } else {
            memory.remove("x");
        }

        System.out.println("Graficando f(x) = " + exprText + " en [" + xmin + ", " + xmax + "] (" + xs.size() + " puntos validos)...");
        new PlotWindow(xs, ys, exprText);
        return 0.0;
    }

    // Comando plot(expr, xmin, xmax, ymin, ymax) - Reto 3
    @Override
    public Double visitPlotRangeExpr(ScientificCalcParser.PlotRangeExprContext ctx) {
        String exprText = ctx.expr(0).getText();
        Double xmin = visit(ctx.expr(1));
        Double xmax = visit(ctx.expr(2));
        Double ymin = visit(ctx.expr(3));
        Double ymax = visit(ctx.expr(4));

        if (xmin == null || xmax == null || ymin == null || ymax == null) {
            System.err.println("Error: Parametros de rango de graficacion invalidos.");
            return null;
        }

        int samples = 800;
        List<Double> xs = new ArrayList<>(samples);
        List<Double> ys = new ArrayList<>(samples);

        Double previousX = memory.get("x");

        for (int i = 0; i < samples; i++) {
            double x = xmin + (double) i * (xmax - xmin) / (samples - 1);
            memory.put("x", x);
            Double y = visit(ctx.expr(0));

            if (y != null && Double.isFinite(y)) {
                xs.add(x);
                ys.add(y);
            }
        }

        if (previousX != null) {
            memory.put("x", previousX);
        } else {
            memory.remove("x");
        }

        System.out.println("Graficando f(x) = " + exprText + " con rango Y [" + ymin + ", " + ymax + "]...");
        new PlotWindow(xs, ys, exprText, ymin, ymax);
        return 0.0;
    }

    // Potencia: expr '^' expr (asociativa por la derecha)
    @Override
    public Double visitPower(ScientificCalcParser.PowerContext ctx) {
        Double base = visit(ctx.expr(0));
        Double exponent = visit(ctx.expr(1));
        if (base == null || exponent == null) return null;
        return Math.pow(base, exponent);
    }

    // Operador unario: '+' expr | '-' expr
    @Override
    public Double visitUnary(ScientificCalcParser.UnaryContext ctx) {
        Double value = visit(ctx.expr());
        if (value == null) return null;
        if (ctx.op.getText().equals("-")) {
            return -value;
        }
        return value;
    }

    // Multiplicacion y Division: expr op=('*'|'/') expr
    @Override
    public Double visitMulDiv(ScientificCalcParser.MulDivContext ctx) {
        Double left = visit(ctx.expr(0));
        Double right = visit(ctx.expr(1));
        if (left == null || right == null) return null;

        if (ctx.op.getType() == ScientificCalcParser.MUL) {
            return left * right;
        } else {
            if (right == 0.0) {
                System.err.println("Error semantico: Division por cero en '" + ctx.getText() + "'.");
                return null;
            }
            return left / right;
        }
    }

    // Suma y Resta: expr op=('+'|'-') expr
    @Override
    public Double visitAddSub(ScientificCalcParser.AddSubContext ctx) {
        Double left = visit(ctx.expr(0));
        Double right = visit(ctx.expr(1));
        if (left == null || right == null) return null;

        if (ctx.op.getType() == ScientificCalcParser.ADD) {
            return left + right;
        } else {
            return left - right;
        }
    }

    // Funciones cientificas de 1 argumento
    @Override
    public Double visitFunctionCall(ScientificCalcParser.FunctionCallContext ctx) {
        String func = ctx.function().getText();
        Double value = visit(ctx.expr());
        if (value == null) return null;

        switch (func) {
            case "sin":   return Math.sin(value);
            case "cos":   return Math.cos(value);
            case "tan":   return Math.tan(value);
            case "asin":  return Math.asin(value);
            case "acos":  return Math.acos(value);
            case "atan":  return Math.atan(value);
            case "sqrt":
                if (value < 0) {
                    System.err.println("Error semantico: Raiz cuadrada de numero negativo en '" + ctx.getText() + "'.");
                    return null;
                }
                return Math.sqrt(value);
            case "log":
                if (value <= 0) {
                    System.err.println("Error semantico: Logaritmo de valor menor o igual a cero en '" + ctx.getText() + "'.");
                    return null;
                }
                return Math.log10(value);
            case "ln":
                if (value <= 0) {
                    System.err.println("Error semantico: Logaritmo natural de valor menor o igual a cero en '" + ctx.getText() + "'.");
                    return null;
                }
                return Math.log(value);
            case "abs":   return Math.abs(value);
            case "exp":   return Math.exp(value);
            case "floor": return Math.floor(value);
            case "ceil":  return Math.ceil(value);
            default:
                System.err.println("Error: Funcion desconocida '" + func + "'.");
                return null;
        }
    }

    // Funciones cientificas de 2 argumentos (Reto 2)
    @Override
    public Double visitFunctionCall2(ScientificCalcParser.FunctionCall2Context ctx) {
        String func = ctx.function2().getText();
        Double arg1 = visit(ctx.expr(0));
        Double arg2 = visit(ctx.expr(1));
        if (arg1 == null || arg2 == null) return null;

        switch (func) {
            case "pow": return Math.pow(arg1, arg2);
            case "max": return Math.max(arg1, arg2);
            case "min": return Math.min(arg1, arg2);
            default:
                System.err.println("Error: Funcion binaria desconocida '" + func + "'.");
                return null;
        }
    }

    // Constantes matematicas: pi, e
    @Override
    public Double visitConstantExpr(ScientificCalcParser.ConstantExprContext ctx) {
        String name = ctx.constant().getText();
        if (name.equals("pi")) {
            return Math.PI;
        } else if (name.equals("e")) {
            return Math.E;
        }
        return 0.0;
    }

    // Numeros reales (enteros y decimales)
    @Override
    public Double visitNumber(ScientificCalcParser.NumberContext ctx) {
        return Double.parseDouble(ctx.NUMBER().getText());
    }

    // Identificador / Variable
    @Override
    public Double visitId(ScientificCalcParser.IdContext ctx) {
        String id = ctx.ID().getText();
        if (memory.containsKey(id)) {
            return memory.get(id);
        }
        System.err.println("Error semantico: Variable '" + id + "' no definida. Se asume 0.0.");
        return 0.0;
    }

    // Parentesis
    @Override
    public Double visitParens(ScientificCalcParser.ParensContext ctx) {
        return visit(ctx.expr());
    }

    // Linea en blanco
    @Override
    public Double visitBlank(ScientificCalcParser.BlankContext ctx) {
        return 0.0;
    }
}
