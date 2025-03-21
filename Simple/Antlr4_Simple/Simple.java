/**
 * Técnicas de Compilação
 * Mestrado em Engenharia Informática
 * Faculdade de Ciências
 * Universidade de Lisboa
 * 2024/2025
 * 
 * As per "The Definitive ANTLR 4 Reference",
 * but using CharStreams in place of the deprecated ANTLRInputStream
 * 
 * Run as:
 *
 * $ antlr4 Simple.g4
 * $ javac *java
 * $ java Simple < ../example.simple
 */
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class Simple {
    public static void main(String[] args) throws Exception {
        // create a CharStream that reads from standard input
        CharStream input = CharStreams.fromStream(System.in);
        // create a lexer that feeds off of input CharStream
        SimpleLexer lexer = new SimpleLexer(input);
        // create a buffer of tokens pulled from the lexer
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        // create a parser that feeds off the tokens buffer
        SimpleParser parser = new SimpleParser(tokens);
        ParseTree tree = parser.exp(); // begin parsing at init rule
        System.out.println(tree.toStringTree(parser)); // print LISP-style tree
    }
}
