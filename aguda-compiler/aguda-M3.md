# AGUDA Compiler

- **AGUDA Language Author:** tcomp000, Vasco T. Vasconcelos
- **Compiler Author:** 58182, Gabriel Henriques

This project is a compiler for the AGUDA programming language, built using PLY. For now, it includes a lexer, a parser and type checker. The compiler also supports running tests for valid and invalid programs.

## How to build the compiler
- **Ensure you have Docker installed and running**
- **Run the following command** (inside project's root folder):

        TODO

- When you no longer need the docker, you may remove the image by executing:

        docker rmi aguda-compiler

## How to run a particular test
run the following command:

    TODO

Example:

    TODO

It's also possible to run without arguments and write the AGUDA program directly in the console, followed by [ENTER] and Ctrl+D (EOF):

    TODO


### How to interpret particular test output
After running a particular **valid** test, the compiler outputs the textual representation of its AST, for example, the following command:

    docker-compose run --rm aguda-compiler test/valid/tcomp000_powers/powers.agu

Should produce the following output:

    let powers(n) : (Int) -> Int[] =
    let a : Int[] =
        new Int [n | 0] ;
        let i : Int =
        0 ;
        while i < n do
            set a[i] = i * i ;
            a
    let _ : Unit =
    print(powers(10))

If the given test is **invalid**, the compiler outputs what it was able to parse and also the syntatic and/or lexer errors that are present in the test program. For example, the following program:

    -- Author: 58250, Leonardo Monteiro

    -- Function to convert euros to dollars
    let euros_to_usd (euros : Float) : Float = euros * 1.18

    let amount_euros : Float = 100  -- Amount in euros
    let amount_usd : Float = euros_to_usd(amount_euros)

    let _ : Unit = 
        print(amount_usd)    -- Expected result: 118.0 


Should produce the following output:

    Syntactic error: at line 4, column 25: Unexpected token ':'
    Lexical error: Illegal character '.' at line 4, column 53
    Syntactic error: at line 6, column 20: Unexpected token 'Float'
    Syntactic error: at line 7, column 18: Unexpected token 'Float'
    let _ : Unit =
        print(amount_usd)

# How to run the whole test suit

To run the whole test suit, the following command must be executed:

    TODO --suite

The tests should be put separated into three different subdirectories depending on their type:
- Valid tests -> `test\valid`
- Semantic invalid tests -> `test\invalid-semantic`
- Syntatic invalid tests -> `test\invalid-syntax`

Each program (valid or invalid) must be included in a distinct folder. Valid test folders should contain two files. For a program `p`, include a `p.agu` (the source code) and a `p.expect` (a txt file with the expected output of program `p`). Folders for invalid tests contain one `.agu` file only. Resulting in the following directory schema:

    project_root\
    ├── test\
        ├── invalid-semantic\
        │   ├── tcomp000-while-plus-five0\
        |   |   ├── while-plus-five.agu
        |   |...
        |
        ├── invalid-syntax\
        │   ├── tcomp000_wrong_comment\
        |   |   ├── wrong_comment.agu
        |   |...
        |
        └── valid\
            ├── tcomp000_powers\
            |   ├── powers.agu
            |   ├── powers.expect
            |...

### How to interpret the test suit output

The test suit generates three different logs inside the folder `test/logs`, one for each type of test. Each log consists of the following:
- Log header:
    
    - Type-of-test
    - Number of passed tests `[✔]`
    - Number of failed tests `[FAIL]`

- For each test file:

    - Filepath
    - Test result: 
        
        - Passed `[✔]` (if **valid** test and **semantically correct** OR if **invalid** test and **semantically incorrect**)

        - Failed `[FAIL]` (if **valid** test and it **semantically inorrect** OR if **invalid** test and it **semantically correct**)
    - Test errors:

        - If **valid** test and **semantically incorrect**:

                test\valid\58219_logical_operators\logical_operators.agu [FAIL]
                Semantic Error: (9, 5) number of params does not match type in function declaration 'notOp'
                Semantic Error: (17, 9) expected arguments of types [Bool, Bool], found [Bool] for expression 
                'notOp(true)'
                Semantic Error: (18, 9) expected arguments of types [Bool, Bool], found [Bool] for expression 
                'notOp(false)'

        - If **invalid** test and **semantically correct**

                test\invalid-semantic\64371_variable_not_in_scope\variable_not_in_scope.agu [FAIL]
                Expected error but none found.

        - If **invalid** test and **semantically incorrect**

                test\invalid-semantic\tcomp000-while-plus-five\while-plus-five.agu [✔]
                Semantic Error: (3, 16) Expected type 'Int', found type 'Unit' for expression 
                'while false do 5'

## How to change the max number of errors to be printed
To change the max number of errors to be printed you just need to changed the value of the constant `MAX_ERRORS` at the top of the file `type_checker.py`.

## A brief description of how you implemented the symbol table

The Symbol Table was implemented as a hierarchical structure, it uses a dictionary to store symbols in the current scope and supports nested scopes through a parent-child relationship.

Methods:

- `insert`: Adds a symbol and its type to the current scope.
- `lookup`: Searches for a symbol in the current scope and recursively in parent scopes if not found in the current one.
- `enter_scope`: When called returns a new `SymbolTable` child scope linked to the current scope.

## A brief description of how you implemented bidirectional type checking

Bidirectional type checking was implemented using two main functions: `typeof` for type synthesis and `checkAgainst` to analyse an expression against a given type. These functions are mutually recursive and rely heavily on Python's pattern matching to handle different expression forms.

`checkAgainst` uses pattern matching to directly analyze expressions like conditionals, assignments, and function calls against expected types. This avoids generic error messages and allows precise error reporting. In contrast, `typeof` is used when no expected type is given and returns the inferred type of the expression.

Several helper functions support this logic, including `checkEqualTypes` for comparing types, `checkInstance` to check if a type is an instance of another type, and `checkArguments` for validating function call arguments. These help centralize common checks and keep the two main functions clean.

## If your program does not pass all tests, explain why

- My type checker currently has the same tests results as the professor's, so the tests that fail are, supposedly, incorrectly written.