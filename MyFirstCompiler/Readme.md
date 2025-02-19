Técnicas de Compilação\
Mestrado em Engenharia Informática\
Faculdade de Ciências\
Universidade de Lisboa\
2024/2025\
Alcides Fonseca\
Vasco Vasconcelos

# My First Compiler

## Overview

This project shows an example of a compiler pipeline.

The frontend is responsible for parsing the input file (example.lang) and returning an AST.

Two implementations are provided: Haskell and Python.

In Python, the AST is designed using an OO approach, with two main types (Statement and Expression), and multiple options for each. In Haskell Statements and Expressions atre datatypes.In any case, a program is a list of statements.

There is one semantic validation: detecting whether variables are used before being defined.

There are two backends: one that interprets the program by tree-walking, and another that translates the tree to C, and uses the gcc compiler to obtain a binary file. This backend has one optimization: if the program contains the sum of two literals, the sum happens at compiler time, not in the final binary.

## Usage

```
$ runHaskell Main example.lang
$ ./executable
```
or
```
$ python3 main.py example.lang
$ ./executable
```

## Limitations

The parser performs string splitting — this is not how one writes parsers! We want to able to write things like `1 + 2 + 3` or use other operators with precedence. We will cover parser generators later in the course.

If our language features types other than integers, validation should focus on typechecking as well: checking that all values have the expected type.

Finally, this language is very similar to C, so our backend is not very interesting. Backends require more effort when the intermediate language (or AST) has a higher level of abstraction that the target language.