import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.InputStream;
import java.io.FileInputStream;

public class Main {
    public static void main(String[] args) throws Exception {
        InputStream is = System.in;
        if (args.length > 0) {
            is = new FileInputStream(args[0]);
        }

        CharStream input = CharStreams.fromStream(is);
        ScientificCalcLexer lexer = new ScientificCalcLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        ScientificCalcParser parser = new ScientificCalcParser(tokens);

        ParseTree tree = parser.prog();

        if (parser.getNumberOfSyntaxErrors() == 0) {
            ScientificEvalVisitor visitor = new ScientificEvalVisitor();
            visitor.visit(tree);
        } else {
            System.err.println("Se detectaron errores sintacticos en la entrada.");
        }
    }
}
