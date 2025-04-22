import os
import io
import contextlib
from src.lexer import lexer
from src.parser import parser, reset_parser
from src.type_checker import SemanticError, verify
import sys

TEST_DIR = 'test'
LOG_DIR = os.path.join(TEST_DIR, 'logs')
VALID_DIR = os.path.join(TEST_DIR, 'valid')
INVALID_SEM_DIR = os.path.join(TEST_DIR, 'invalid-semantic')
INVALID_SYN_DIR = os.path.join(TEST_DIR, 'invalid-syntax')

def write_logs(logs, test_type):

    log_path = os.path.join(LOG_DIR, f'{test_type}.log')
    os.makedirs(LOG_DIR, exist_ok=True)

    passed = sum(1 for line in logs if '[✔]' in line)
    failed = sum(1 for line in logs if '[FAIL]' in line or '[EXCEPTION]' in line)

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(test_type + '\n\n')
        f.write(f"Passed [✔]: {passed}\n")
        f.write(f"Failed [FAIL]: {failed}\n\n")
        for line in logs:
            f.write(line + '\n')

    print(f"Logs written to {log_path}")

def syntax_test_run(filepath, valid, print_ast=False):

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
        if print_ast:
            print(ast)
        output = output_buffer.getvalue().strip()
    except Exception as e:
        test_log.append(f"{filepath} [EXCEPTION]")
        test_log.append(str(e))
        return test_log

    if valid:
        if output == "":
            # No errors printed -> Test passed
            test_log.append(f"{filepath} [✔]")
        else:
            # Expected no output, but got errors
            test_log.append(f"{filepath} [FAIL]")
            test_log.append(output)
    else:
        if output == "":
            # Expected errors, but got none
            test_log.append(f"{filepath} [FAIL]")
            test_log.append("Expected error but none found.")
        else:
            # Errors printed as expected
            test_log.append(f"{filepath} [✔]")
            test_log.append(output)
    
    return test_log

def semantic_test_run(filepath, valid, print_ast=False):

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

        if print_ast:
            print(ast)
        output = output_buffer.getvalue().strip()

    except Exception as e:
        test_log.append(f"{filepath} [EXCEPTION]")
        test_log.append(str(e))
        return test_log

    # If there are syntax errors, exit without semantic validation
    if output:
        test_log.append(f"{filepath} [FAIL]")
        test_log.append(output)
        return test_log

    # Perform semantic validation if no syntax errors
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            verify(ast)

    except SemanticError as e:
        output = output_buffer.getvalue().strip()
        if valid:
            test_log.append(f"{filepath} [FAIL]")
            test_log.append(output)
        else:
            test_log.append(f"{filepath} [✔]")
            test_log.append(output)
        return test_log    
        
    except Exception as e:
        output = output_buffer.getvalue().strip()
        test_log.append(f"{filepath} [EXCEPTION]")
        test_log.append(str(e))
        return test_log
    
    output = output_buffer.getvalue().strip()
    if valid:
        test_log.append(f"{filepath} [✔]")
        test_log.append(output)
    else:
        test_log.append(f"{filepath} [FAIL]")
        test_log.append("Expected error but none found.")
    
    return test_log

def run_multiple_tests(test_dir : str, valid : bool, type : int):
    """
    Run multiple tests in a directory.
    :param test_dir: Directory containing the tests
    :param valid: True if the programs to test are valid, False if they are invalid
    :param type: 0 for syntax tests, 1 for semantic tests
    :return: List logs of the tests
    """
    logs = []

    all_files = []
    for root, _, files in os.walk(test_dir):
        all_files.extend(os.path.join(root, file) for file in files if file.endswith('.agu'))

    all_files.sort()

    for filepath in all_files:
        if type == 0:
            test_log = syntax_test_run(filepath, valid)
            test_log.append("\n")
        else:
            test_log = semantic_test_run(filepath, valid)
            test_log.append("\n")

        logs.extend(test_log)

    return logs

def run_test_suite():
    invalid_sem_tests_logs = run_multiple_tests(INVALID_SEM_DIR, valid=False, type=1)
    write_logs(invalid_sem_tests_logs, "invalid-semantic-tests")

    invalid_syn_tests_logs = run_multiple_tests(INVALID_SYN_DIR, valid=False, type=0)
    write_logs(invalid_syn_tests_logs, "invalid-syntax-tests")

    valid_tests_logs = run_multiple_tests(VALID_DIR, valid=True, type=1)
    write_logs(valid_tests_logs, "valid-tests")

def run_single_test(filepath):
    """
    Run a single test.
    :param filepath: Path to the test file
    """
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return
    if not filepath.endswith('.agu'):
        print(f"File '{filepath}' is not a .agu file.")
        return
    else:
        print(f"Running test: {filepath}")
        test_log = semantic_test_run(filepath, valid=True, print_ast=True)
        print(test_log[1])

def main():
    # If no args, accept stdin as program input
    if len(sys.argv) == 1:
        print("Write the AGUDA code to be validated, followed by [ENTER] and Ctrl+D (EOF)")
        code = sys.stdin.read()
        temp_file_path = os.path.join(TEST_DIR, 'temp_input.agu')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(code)
        run_single_test(temp_file_path)
        os.remove(temp_file_path)
    
    elif len(sys.argv) == 2:
        # If the first argument is --suite, run all tests
        if sys.argv[1] == "--suite":
            print("Running all tests...")
            run_test_suite()
        
        elif sys.argv[1] == "--help":
            print("Usage: docker-compose run --rm aguda-compiler [<file_path> | --tests]")
            return
        
        # If the first argument is a file path, run that test
        else:
            filepath = sys.argv[1]
            if not os.path.isfile(filepath):
                print(f"File '{filepath}' does not exist.")
                return
            run_single_test(filepath)
    else:
        print("Usage: docker-compose run --rm aguda-compiler [<file_path> | --tests]")

if __name__ == '__main__':
    main()
    #run_test_suite()
    #run_single_test(r".\test\valid\54394_zip\zip.agu")