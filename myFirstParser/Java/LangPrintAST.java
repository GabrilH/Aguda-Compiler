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
 * See Lang.g4 on how to generate Java from a g4 grammar. Then
 * 
 * Run as:
 *
 * $ antlr4 Lang.g4
 * $ javac *java
 * $ java LangPrintAST < example.lang 
 */
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class LangPrintAST {
    public static void main(String[] args) throws Exception {
        // create a CharStream that reads from standard input
        CharStream input = CharStreams.fromStream(System.in);
        // create a lexer that feeds off of input CharStream
        LangLexer lexer = new LangLexer(input);
        // create a buffer of tokens pulled from the lexer
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        // create a parser that feeds off the tokens buffer
        LangParser parser = new LangParser(tokens);
        ParseTree tree = parser.lang(); // begin parsing at init rule
        System.out.println(tree.toStringTree(parser)); // print LISP-style tree
    }
}
