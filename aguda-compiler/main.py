import argparse
import os
import io
import subprocess
import contextlib
from pathlib import PureWindowsPath, PurePosixPath
from src.code_generator import CodeGenerator, CodeGenerationError
from src.lexer import lexer
from src.parser import parser, reset_parser
from src.type_checker import SemanticError, TypeChecker
import sys

LOG_DIR = os.path.join(os.getcwd(), 'logs')
TEST_DIR = os.path.join(os.getcwd(), "aguda-testing", "test")
VALID_DIR = os.path.join(TEST_DIR, 'valid')
INVALID_SEM_DIR = os.path.join(TEST_DIR, 'invalid-semantic')
INVALID_SYN_DIR = os.path.join(TEST_DIR, 'invalid-syntax')
MAX_ERRORS = 5
TOTAL_TESTS = 0
TOTAL_FAILED_TESTS = 0

def write_logs(logs, test_type):

    log_path = os.path.join(LOG_DIR, f'{test_type}.log')
    os.makedirs(LOG_DIR, exist_ok=True)

    passed = sum(1 for line in logs if '[✔]' in line)
    failed = sum(1 for line in logs if '[FAIL]' in line or '[EXCEPTION]' in line)
    total = passed + failed

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(test_type + '\n\n')
        f.write(f"Total tests run: {total}\n")
        f.write(f"Passed [✔]: {passed}\n")
        f.write(f"Failed [FAIL]: {failed}\n\n")
        for line in logs:
            f.write(line + '\n')

    print(f"Logs written to {log_path}")

def syntax_test_run(filepath, valid):

    test_log = []
    
    with open(filepath, 'r') as f:
        code = f.read()

    # Reset the parser (for the line counter)
    reset_parser()

    # Store stdout of parser
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            ast = parser.parse(code, lexer=lexer)
    except Exception as e:
        test_log.append(f"{filepath} [EXCEPTION]")
        test_log.append(str(e))
        return test_log, ast

    output = output_buffer.getvalue().strip()
    if valid:
        if output == "":
            # No errors printed -> Test passed
            test_log.append(f"{filepath} [✔]")
        else:
            # Found errors -> Test failed
            test_log.append(f"{filepath} [FAIL]")
            test_log.append(output)
    else:
        if output == "":
            # Expected errors, but got none -> Test failed
            test_log.append(f"{filepath} [FAIL]")
            test_log.append("Expected error but none found.")
        else:
            # Expected errors and got them -> Test passed
            test_log.append(f"{filepath} [✔]")
            test_log.append(output)
    
    return test_log, ast

def semantic_test_run(filepath, valid):

    syntax_log, ast = syntax_test_run(filepath, True)

    # If there are syntax errors, exit without semantic validation
    if any("[FAIL]" in line or "[EXCEPTION]" in line for line in syntax_log):
        return syntax_log, ast

    test_log = []

    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            TypeChecker(MAX_ERRORS).verify(ast)
    except SemanticError as e:
        pass_status = "[✔]" if not valid else "[FAIL]"
        test_log.append(f"{filepath} {pass_status}")
        test_log.append(output_buffer.getvalue().strip())
        return test_log, ast    
        
    except Exception as e:
        test_log.append(f"{filepath} [EXCEPTION]")
        test_log.append(str(e))
        return test_log, ast
    
    pass_status = "[✔]" if valid else "[FAIL]"
    test_log.append(f"{filepath} {pass_status}")
    test_log.append(output_buffer.getvalue().strip() if valid else "Expected error but none found.")
    
    return test_log, ast

def code_gen_test_run(filepath, valid):
    
    semantic_log, ast = semantic_test_run(filepath, True)

    # If there are semantic errors, exit without code generation
    if any("[FAIL]" in line or "[EXCEPTION]" in line for line in semantic_log):
        return semantic_log, ast
    
    test_log = semantic_log # TODO: change to []
    # output_path = filepath.replace('.agu', '.ll')
    
    # try:
    #     code_gen = CodeGenerator(MAX_ERRORS)
    #     llvm_ir = code_gen.generate(ast)
        
    #     with open(output_path, 'w') as f:
    #         f.write(llvm_ir)
        
    #     # Now run the LLVM IR using lli
    #     result = subprocess.run(['lli', output_path], capture_output=True, text=True)

    #     expect_path = filepath.replace('.agu', '.expect')
            
    #     try:
    #         with open(expect_path, 'r') as f:
    #             expected_output = f.readline().strip()
            
    #         actual_output = result.stdout.strip()
            
    #         if actual_output == expected_output:
    #             test_log.append(f"{filepath} [✔]")
    #         else:
    #             test_log.append(f"{filepath} [FAIL]")
    #             test_log.append(f"Expected: '{expected_output}'")
    #             test_log.append(f"Got: '{actual_output}'")

    #     except FileNotFoundError:
    #         test_log.append(f"{filepath} [FAIL]")
    #         test_log.append(f"Expect file not found: {expect_path}")

    # except CodeGenerationError as e:
    #     test_log.append(f"{filepath} [SKIP]")
    #     test_log.append(str(e))
    # except Exception as e:
    #     test_log.append(f"{filepath} [EXCEPTION]")
    #     test_log.append(str(e))
    
    return test_log, ast

def run_multiple_tests(test_dir : str, valid : bool, type : int):
    """
    Run multiple tests in a directory.
    :param test_dir: Directory containing the tests
    :param valid: True if the programs to test are valid, False if they are invalid
    :param type: 0 for syntax tests, 1 for semantic tests, 2 for code generation tests
    :return: List logs of the tests
    """
    global TOTAL_TESTS, TOTAL_FAILED_TESTS

    logs = []

    all_files = []
    for root, _, files in os.walk(test_dir):
        all_files.extend(os.path.join(root, file) for file in files if file.endswith('.agu'))

    all_files.sort()

    for filepath in all_files:
        TOTAL_TESTS += 1
        if type == 0:
            test_log,_ = syntax_test_run(filepath, valid)
            test_log.append("\n")
        elif type == 1:
            test_log,_ = semantic_test_run(filepath, valid)
            test_log.append("\n")
        elif type == 2:
            test_log,_ = code_gen_test_run(filepath, valid)
            test_log.append("\n")

        if any("[FAIL]" in line or "[EXCEPTION]" in line for line in test_log):
            TOTAL_FAILED_TESTS += 1 

        logs.extend(test_log)

    return logs

def run_test_suite():

    global TOTAL_TESTS, TOTAL_FAILED_TESTS

    TOTAL_TESTS = 0
    TOTAL_FAILED_TESTS = 0

    invalid_sem_tests_logs = run_multiple_tests(INVALID_SEM_DIR, valid=False, type=1)
    write_logs(invalid_sem_tests_logs, "invalid-semantic-tests")

    invalid_syn_tests_logs = run_multiple_tests(INVALID_SYN_DIR, valid=False, type=0)
    write_logs(invalid_syn_tests_logs, "invalid-syntax-tests")

    valid_tests_logs = run_multiple_tests(VALID_DIR, valid=True, type=2)
    write_logs(valid_tests_logs, "valid-tests")

    print(f"\nTest Suite Summary:")
    print(f"Total Tests Run: {TOTAL_TESTS}")
    print(f"Total Passed Tests: {TOTAL_TESTS - TOTAL_FAILED_TESTS}")
    print(f"Total Failed Tests: {TOTAL_FAILED_TESTS}")

def run_single_test(filepath):
    """
    Run a single test.
    :param filepath: Path to the test file
    """
    filepath = str(PurePosixPath(PureWindowsPath(filepath)))
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return
    if not filepath.endswith('.agu'):
        print(f"File '{filepath}' is not a .agu file.")
        return
    else:
        test_log, ast = code_gen_test_run(filepath, valid=True)
        print(ast)
        print(test_log[1])

def main():
    global MAX_ERRORS
    args_parser = argparse.ArgumentParser(description="AGUDA Compiler")
    args_parser.add_argument("--suite", action="store_true", help="Run all tests")
    args_parser.add_argument("--max_errors", type=int, default=MAX_ERRORS, help="Set the maximum number of errors allowed")
    args_parser.add_argument("file_path", nargs="?", help="Path to the AGUDA file to test (optional)")

    args = args_parser.parse_args()

    if args.max_errors < 0:
        print("max_errors must be a non-negative integer.")
        return
    MAX_ERRORS = args.max_errors

    if args.suite:
        print(f"Running all tests with max_errors={MAX_ERRORS}")
        run_test_suite()
        return
    
    if args.file_path:
        print(f"Running single test on file '{args.file_path}' with max_errors={MAX_ERRORS}")
        run_single_test(args.file_path)
        return

    # Default behavior: accept stdin as program input
    print(f"Write the AGUDA code to be validated, followed by [ENTER] and Ctrl+D (EOF). Max errors allowed: {MAX_ERRORS}")
    code = sys.stdin.read()
    temp_file_path = os.path.join(TEST_DIR, 'temp_input.agu')
    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(code)
    run_single_test(temp_file_path)
    os.remove(temp_file_path)

if __name__ == '__main__':
    #main()
    run_test_suite()
    #run_single_test(r".\test\valid\64854_printA\printA.agu")