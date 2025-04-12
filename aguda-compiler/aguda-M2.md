# AGUDA Compiler

- **AGUDA Language Author:** tcomp000, Vasco T. Vasconcelos
- **Compiler Author:** 58182, Gabriel Henriques

This project is a compiler for the AGUDA programming language, built using PLY. For now, it includes a lexer and a parser. The compiler also supports running tests for valid and invalid programs.

## How to build the compiler
- **Ensure you have Docker installed and running**
- **Run the following command** (inside `/aguda-compiler` folder):

        docker-compose build

- When you no longer need the docker, you may remove the image by executing:

        docker rmi aguda-compiler

## How to run a particular test
After building the docker image, you should put the program to test inside the `/test` folder, or their subdirectories, and run the following command:

    docker-compose run --rm aguda-compiler TEST_PATH

Example:

    docker-compose run --rm aguda-compiler test/valid/tcomp000_powers/powers.agu

It's also possible to run without arguments and write the AGUDA program directly in the console, followed by [ENTER] and Ctrl+D (EOF):

    docker-compose run --rm aguda-compiler

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

    docker-compose run --rm aguda-compiler --tests 

The tests should be put separated into three different subdirectories depending on their type:
- Valid tests -> `test\valid`
- Semantic invalid tests -> `test\invalid-semantic`
- Syntatic invalid tests -> `test\invalid-syntax`

Each program (valid or invalid) must be included in a distinct folder. Valid test folders should contain two files. For a program `p`, include a `p.agu` (the source code) and a `p.expect` (a txt file with the expected output of program `p`). Folders for invalid tests contain one `.agu` file only. Resulting in the following directory schema:

    aguda-compiler\
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
        
        - Passed `[✔]` (if **valid** test and **parses** OR if **invalid** test and it **doesn't parse**)

        - Failed `[FAIL]` (if **valid** test and it **doesn't parse** OR if **invalid** test and it **parses**)
    - Test errors:

        - If **valid** test and it **doesn't parse**:

                test/valid/58250_euros_to_usd/58250_euros_to_usd.agu [FAIL]
                Syntactic error: at line 4, column 25: Unexpected token ':'
                Lexical error: Illegal character '.' at line 4, column 53
                Syntactic error: at line 6, column 20: Unexpected token 'Float'
                Syntactic error: at line 7, column 18: Unexpected token 'Float'

        - If **invalid** test and it **parses**

                test/invalid-syntax/58166_sumIntBool/sumIntBool.agu [FAIL]
                Expected error but none found.

        - If **invalid** test and it **doesn't parse**

                test/invalid-syntax/tcomp000_wrong_comment/wrong_comment.agu [✔]
                Lexical error: Illegal character '#' at line 3, column 1
                Syntactic error: at line 3, column 3: Unexpected token 'Comments'

## Comments/TODOs

- The parser is currently not accepting functions as parameters of functions, e.g. it doesn't parse the following program:

        -- Author: tcomp56311, João Vedor

        let apply(f, x) : (Int -> Int, Int) -> Int = 
            f(x)

        let double(x) : Int -> Int = 
            x * 2

        let result : Int = 
            apply(double, 21)

        let main : Unit = 
            print(result)

    Resulting in the following output:

        test/valid/56311_high_order_function_type/high_order_func_type.agu [FAIL]
        Syntactic error: at line 3, column 24: Unexpected token '->'

- The parser does not accept unary function types:

        -- Author: fc56334, Goncalo Lopes

        let buildArray(_) : Unit =
            let array : Int[] = new Int [10 | 0];
            set array[0] = 3;
            set array[1] = 2;
            set array[2] = 4;
            set array[3] = 7;
            set array[4] = 1;
            set array[5] = 6;
            set array[6] = 8;
            set array[7] = 9;
            set array[8] = 2;
            set array[9] = 5;
            array
        (...)

    Resulting in the following output:

        test/valid/56334_bubbleSort/bubbleSort.agu [FAIL]
        Syntactic error: at line 3, column 26: Unexpected token '='