# AGUDA Compiler

- **AGUDA Language Author:** tcomp000, Vasco T. Vasconcelos
- **Compiler Author:** 58182, Gabriel Henriques
- **PLY**: https://github.com/dabeaz/ply
- **LLVMLITE:** https://github.com/numba/llvmlite

This project is a compiler for the AGUDA programming language. It includes a lexer, a parser (both made with PLY), a type checker and generates LLVM code via llvmlite binding. The compiler also supports running tests for valid and invalid programs.

You can find the AGUDA language description and each milestone information inside `docs` directory.

**Final Grade:** 19/20


## How to update your tests (**needs FCUL VPN**)
- **Git pull `aguda-testing`**

        cd aguda-testing; git pull

    **OR** (if `aguda-testing` directory does not yet exist) run in project's root folder

        git clone https://git.alunos.di.fc.ul.pt/tcomp000/aguda-testing  

## How to build the compiler
- **Ensure you have Docker installed and running**
        
- **Run the following command** (inside project's root folder):

        docker-compose build

    No-cache building time is taking me a mininum of 1 minute, but it may take more time depending on network speed.

- When you no longer need the docker, you may remove the image by executing:

        docker rmi aguda-compiler

## How to run the whole test suit

To run the whole test suit, the following command must be executed:

    docker-compose run --rm aguda-compiler --suite

The tests should be put separated into three different subdirectories depending on their type:
- Valid tests -> `aguda-testing\test\valid`
- Semantic invalid tests -> `aguda-testing\test\invalid-semantic`
- Syntatic invalid tests -> `aguda-testing\test\invalid-syntax`
- Valid not implemented tests -> `aguda-testing\test\valid-not-implemented`

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

## How to run a particular test
The test to be run should be inside the directory `aguda-testing\test` and be put there **before** building the docker.

    docker-compose run --rm aguda-compiler RELATIVE_TEST_PATH

Example:

    docker-compose run --rm aguda-compiler aguda-testing\test\valid\tcomp000_power-iterative\power-iterative.agu  


## How to interpret particular test output
After running a particular **valid** test, the compiler outputs the textual representation of its AST and a message confirming the expected and actual output, for example, the following command:

    docker-compose run --rm aguda-compiler aguda-testing\test\valid\tcomp000_power-iterative\power-iterative.agu

Should produce the following output:

    Generating LALR tables
    Running single test on file 'aguda-testing\test\valid\tcomp000_power-iterative\power-iterative.agu' with max_errors=5
    let power(base, exponent) : (Int, Int) -> Int =
        let result : Int = 1 ;
        while exponent > 0 do (
            set result = result * base ;
            set exponent = exponent - 1
        ) ;
        result
    let main(_) : (Unit) -> Unit =
        print(power(2, 6))
    Expected: '64'
    Got: '64

If the given test has **non-implemented** code (in the code generation phase), the compiler outputs the AST and also the first found instruction it does not implement. For example, the following program:

    -- Author: tcomp000, Vasco T. Vasconcelos

    let buildArray (n) : Int -> Unit[] =
        new Unit [n | while n > 0 do set n = n - 1]

    let main(_) : Unit -> Unit =
        print(buildArray(10))

Should produce the following output:

    Generating LALR tables
    Running single test on file 'aguda-testing\test\valid-not-implemented\tcomp000_arrayOfUnit\arrayOfUnit.agu' with max_errors=5
    let buildArray(n) : (Int) -> Unit[] =
        new Unit [n | while n > 0 do set n = n - 1]
    let main(_) : (Unit) -> Unit =
        print(buildArray(10))
    Not implemented: Generating code for (3, 29) type 'Unit[]'

If the given test is **semantic invalid**, the compiler outputs the AST and also the semantic errors that are present in the test program. For example, the following program:

    -- Author: tcomp000, Vasco T. Vasconcelos

    let f (_) : Int -> Int = 2 * _

Should produce the following output:

    Generating LALR tables
    Running single test on file 'aguda-testing\test\invalid-semantic\tcomp000-wild-on-the-right\wild-on-the-right.agu' with max_errors=5
    let f(_) : (Int) -> Int =
        2 * _
    Semantic Error: (-1, -1) No main function found
    Semantic Error: (3, 30) Wildcard variable '_' cannot be used
    Semantic Error: (3, 30) Expected variable '_' to be of type 'Int', found type 'None'

If the given test is **syntax invalid**, the compiler outputs what it was able to parse and also the syntatic and/or lexer errors that are present in the test program. For example, the following program:

    -- Author: tcomp000, Vasco T. Vasconcelos

    -- # Comments are to start with --, not #

    let x : Int


Should produce the following output:

    Generating LALR tables
    Running single test on file 'aguda-testing/test/invalid-syntax/tcomp000_wrong_comment/wrong_comment.agu' with max_errors=5
    None
    Syntactic error: at EOF

## How to interpret the test suit output

The test suit generates four different logs inside the folder `logs`, one for each type of test. Each log consists of the following:
- Log header:
    
    - Type-of-test
    - Number of total tests
    - Number of passed tests `[✔]`
    - Number of failed tests `[FAIL]`

- For each test:

    - Filepath
    - Test result: 
        - Passed `[✔]`: The program is valid and the actual output matches the expected output
        - Failed `[FAIL]`: The program may be invalid or the outputs do no match

It also prints to the console:

    Test Suite Summary:
    Total Tests Run: 132
    Total Passed Tests: 114
    Total Failed Tests: 18