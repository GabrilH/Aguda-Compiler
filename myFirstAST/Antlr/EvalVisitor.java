/**
 * Técnicas de Compilação
 * Mestrado em Engenharia Informática
 * Faculdade de Ciências
 * Universidade de Lisboa
 * 2024/2025
 * 
 * An visitor to evaluate a tree of the Simple programming language
 */
import java.util.HashMap;
import java.util.Map;

public class EvalVisitor extends SimpleBaseVisitor<Integer> {

    /** "memory" for our calculator; variable/value pairs go here */
    private Map<String, Integer> store = new HashMap<String, Integer>();

    /** INT */
    @Override
    public Integer visitInt(SimpleParser.IntContext ctx) {
        return Integer.valueOf(ctx.INT().getText());
    }

    /** VAR */
    @Override
    public Integer visitVar(SimpleParser.VarContext ctx) {
        String id = ctx.VAR().getText();
        if (store.containsKey(id))
            return store.get(id);
        else {
            System.out.println("Undeclared symbol: " + id);
            return 0;
        }
    }

    /** expr op=('*'|'/') expr */
    @Override
    public Integer visitMultDiv(SimpleParser.MultDivContext ctx) {
        int left = visit(ctx.exp(0)); // get value of left subexpression
        int right = visit(ctx.exp(1)); // get value of right subexpression
        if ( ctx.op.getType() == SimpleParser.MUL )
            return left * right;
        return left / right; // must be DIV
    }

    /** expr op=('+'|'-') expr */
    @Override
    public Integer visitAddSub(SimpleParser.AddSubContext ctx) {
        int left = visit(ctx.exp(0)); // get value of left subexpression
        int right = visit(ctx.exp(1)); // get value of right subexpression
        if ( ctx.op.getType() == SimpleParser.ADD )
            return left + right;
        return left - right; // must be SUB
    }

    /** '-' exp */
    @Override
    public Integer visitUnMinus(SimpleParser.UnMinusContext ctx) {
        return - visit(ctx.exp());
    }

    /** 'let' VAR '=' exp 'in' exp */
    @Override
    public Integer visitLet(SimpleParser.LetContext ctx) {
        String id = ctx.VAR().getText(); // id is left-hand side of '='
        int value = visit(ctx.exp(0)); // compute value of expression on right
        store.put(id, value); // store it in our memory
        // System.out.println(id + " = " + value);
        return visit(ctx.exp(1));
    }

    /** '(' exp ')' */
    @Override
    public Integer visitParens(SimpleParser.ParensContext ctx) {
        return visit(ctx.exp()); // return child expr's value
    }
}