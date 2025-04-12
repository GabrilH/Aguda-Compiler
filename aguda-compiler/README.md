# AGUDA Compiler

- **AGUDA Language Author:** tcomp000, Vasco T. Vasconcelos
- **Compiler Author:** 58182, Gabriel Henriques

This project is a compiler for the AGUDA programming language, built using PLY. For now, it includes a lexer, parser. The compiler also supports running tests for valid and invalid programs.

## How to build the compiler
- **Ensure you have Docker installed**
- **Run the following command** (inside `/aguda-compiler` folder):

    `docker-compose build`
- When you no longer need the docker, remove the image by executing:

    `docker rmi aguda-compiler`

## How to run a particular test
After building the docker image, you should put the program to test inside the `/test` folder, or their subdirectories, and run the following command:

    docker-compose run --rm aguda-compiler TEST_PATH

Example:

    docker-compose run --rm aguda-compiler test/valid/tcomp000_powers/powers.agu

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

The tests should be put separated into three different subdirectories depending on their type:
- Valid tests -> `test\valid`
- Semantic invalid tests -> `test\invalid-semantic`
- Syntatic invalid tests -> `test\invalid-syntax`

Each `.agu` test file is expected to be inside their own folder, e.g. `powers.agu` should be inside the folder `test/valid/tcomp000_powers/`. Also, for the **valid** tests, there should be an extra file with the expected output of the program inside that same folder, e.g. `powers.expect`. Resulting in the following directory schema:

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

The test suit generates three different logs, one for each type of test. The logs consist of the following:
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
