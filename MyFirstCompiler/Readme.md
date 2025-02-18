# My First Compiler


## Overview

This project shows an example of a compiler pipeline.

The frontend is responsible for parsing the input file (example.lang) and returning an AST.
The AST is designed using an OO approach, with two main types (Statement and Expression), and multiple options for each. A program is a list of statements.
There is one semantic validation: we are detecting if variables are used before they are defined. If so, we raise an exception.
There are two backends: one that interprets the program by tree-walking, and another that translates the tree to C, and uses the gcc compiler to obtain a binary file. This backend has one optimization: if you are writing the sum of two literals, the sum happens at compiler time, not in the final binary.


## How to use

```
python main.py example.lang
./executable
```

## Limitations

The parser does string splitting — this is not how you write a parser! You want to able to write things like `1 + 2 + 3` or use other operators with precedence. We will cover parser generators later in the course.

If our program had types other than integers, our semantic check should focus on typechecking: checking that all values have the expected type.

Finally, this language is very similar to C, so our backend is not very interesting. Backends require more effort when the intermediate language (or AST) has a higher level of abstraction that the target language.