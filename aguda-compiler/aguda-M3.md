# AGUDA Compiler

- **AGUDA Language Author:** tcomp000, Vasco T. Vasconcelos
- **Compiler Author:** 58182, Gabriel Henriques

This project is a compiler for the AGUDA programming language, built using PLY. For now, it includes a lexer, a parser and type checker. The compiler also supports running tests for valid and invalid programs.

## How to build the compiler
- **Ensure you have Docker installed and running**
- **Git pull `aguda-testing`**

        cd aguda-testing; git pull

    **OR** (even `aguda-testing` directory does not yet exist) run in project's root folder (**needs FCUL VPN**)

        git clone https://git.alunos.di.fc.ul.pt/tcomp000/aguda-testing  
        
- **Run the following command** (inside project's root folder):

        docker-compose build

- When you no longer need the docker, you may remove the image by executing:

        docker rmi aguda-compiler

## How to run a particular test
The test to be run should be inside the directory `aguda-testing\test` and be put there **before** building the docker.

    docker-compose run --rm aguda-compiler RELATIVE_TEST_PATH

Example:

    docker-compose run --rm aguda-compiler aguda-testing\test\valid\tcomp000_powers\powers.agu    

It's also possible to run without arguments and write the AGUDA program directly in the console, followed by [ENTER] and Ctrl+D (EOF):

    docker-compose run --rm aguda-compiler


### How to interpret particular test output
After running a particular **valid** test, the compiler outputs the textual representation of its AST and a message saying that the program is semantically valid, for example, the following command:

    docker-compose run --rm aguda-compiler aguda-testing\test\valid\tcomp000_powers\powers.agu

Should produce the following output:

    Generating LALR tables
    Running test: aguda-testing/test/valid/tcomp000_powers/powers.agu
    let powers(n) : (Int) -> Int[] =
        let a : Int[] = new Int [n | 0] ;
        let i : Int = 0 ;
        while i < n do (
            set a[i] = i * i ;
            set i = i + 1
        ) ;
        a
    let _ : Unit =
        print(powers(10))
    Program is semantically valid!

If the given test is **syntax invalid**, the compiler outputs what it was able to parse and also the syntatic and/or lexer errors that are present in the test program. For example, the following program:

    -- Author: tcomp000, Vasco T. Vasconcelos

    -- # Comments are to start with --, not #

    let x : Int


Should produce the following output:

    Generating LALR tables
    Running test: aguda-testing/test/invalid-syntax/tcomp000_wrong_comment/wrong_comment.agu
    None
    Syntactic error: at EOF

If the given test is **semantically invalid**, the compiler outputs the AST of the program and the semantic errors it found. For example, the following program:

    -- tcomp000, vasco t. vasconcelos

    let _ : Int = (while false do 5) + 5

Should produce the following output:

    Generating LALR tables
    Running test: aguda-testing/test/invalid-semantic/tcomp000-while-plus-five/while-plus-five.agu
    let _ : Int =
        (
            while false do 5
        ) + 5
    Semantic Error: (3, 16) Expected type 'Int', found type 'Unit' for expression
    'while false do 5'

# How to run the whole test suit

To run the whole test suit, the following command must be executed:

    docker-compose run --rm aguda-compiler --suite

The tests should be put separated into three different subdirectories depending on their type:
- Valid tests -> `aguda-testing\test\valid`
- Semantic invalid tests -> `aguda-testing\test\invalid-semantic`
- Syntatic invalid tests -> `aguda-testing\test\invalid-syntax`

Each program (valid or invalid) must be included in a distinct folder. Valid test folders should contain two files. For a program `p`, include a `p.agu` (the source code) and a `p.expect` (a txt file with the expected output of program `p`). Folders for invalid tests contain one `.agu` file only. Resulting in the following directory schema:

    project_root\
        ├── aguda-testing\
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

The test suit generates three different logs inside the folder `logs`, one for each type of test. Each log consists of the following:
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

                /app/aguda-testing/test/valid/58166_powerTen/powerTen.agu [FAIL]
                Semantic Error: (5, 5) Expected both branches to be of same type; found Int and Unit, for expression 
                'if n < 0 then
                    0 - 1
                else
                    unit'

        - If **invalid** test and **semantically correct**

                /app/aguda-testing/test/invalid-semantic/58166_outOfBounds/outOfBounds.agu [FAIL]
                Expected error but none found.

        - If **invalid** test and **semantically incorrect**

                /app/aguda-testing/test/invalid-semantic/tcomp000-while-plus-five/while-plus-five.agu [✔]
                Semantic Error: (3, 16) Expected type 'Int', found type 'Unit' for expression 
                'while false do 5'

## How to change the max number of errors to be printed
To change the max number of errors to be printed you just need to changed the value of the constant `MAX_ERRORS` at the top of the file `type_checker.py`.

## A brief description of how you implemented the symbol table

The Symbol Table was implemented as a hierarchical structure, it uses a dictionary to store the symbols in the current scope and supports nested scopes through a parent-child relationship.

Methods:

- `insert`: Adds a symbol and its type to the current scope.
- `lookup`: Searches for a symbol in the current scope and recursively in parent scopes if not found in the current one.
- `enter_scope`: When called returns a new `SymbolTable` child scope linked to the current scope.

## A brief description of how you implemented bidirectional type checking

Bidirectional type checking was implemented using two main functions: `typeof` for type synthesis and `checkAgainst` to analyse an expression against a given type. These functions are mutually recursive and rely heavily on Python's pattern matching to handle different expression forms.

`checkAgainst` uses pattern matching to directly analyze expressions like conditionals, assignments, and function calls against expected types. This avoids generic error messages and allows precise error reporting. In contrast, `typeof` is used when no expected type is given and returns the inferred type of the expression.

Several helper functions support this logic, including `checkEqualTypes` for comparing types, `checkInstance` to check if a type is an instance of another type, and `checkArguments` for validating function call arguments. These help centralize common checks and keep the two main functions clean.

## If your program does not pass all tests, explain why

- My type checker currently has three errors difference from the professor's.
    1. The programs `58250_calculate_operations` and `58250_cube` and syntatically valid in my type checker because the wildcard `_` can be used as ID to declare multiple times without problem

    2. My type checker finds the following error in the program `54394_semicolon_assignment`, where the professor's does not find any error.

            -- Author: 54394, Afonso Esteves

            let _ : Int =
                let y : Int = 4;
                while y < 10 do (
                    set y = y + 4
                );
                y

            Semantic Error: (4, 5) Expected type 'Int', found type 'Unit' for expression 'let y : Int = 4'

    This is happening because the expression `let _ : Int =` is expecting to find a type 'Int' in the expression `let y : Int = 4` but it is instead receiving a type 'Unit'.


