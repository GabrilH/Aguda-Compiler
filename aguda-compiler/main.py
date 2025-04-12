import os
import datetime
import io
import contextlib
from src.lexer import lexer
from src.parser import parser, reset_parser
import sys

TEST_DIR = 'test'
LOG_DIR = os.path.join(TEST_DIR, 'logs')
VALID_DIR = os.path.join(TEST_DIR, 'valid')
INVALID_SEM_DIR = os.path.join(TEST_DIR, 'invalid-semantic')
INVALID_SYN_DIR = os.path.join(TEST_DIR, 'invalid-syntax')

def write_logs(logs, header_message):

    today = datetime.date.today().isoformat()
    log_path = os.path.join(LOG_DIR, f'{header_message}-{today}.log')
    os.makedirs(LOG_DIR, exist_ok=True)

    passed = sum(1 for line in logs if '[✔]' in line)
    failed = sum(1 for line in logs if '[FAIL]' in line or '[EXCEPTION]' in line)

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(header_message + '\n\n')
        f.write(f"Passed [✔]: {passed}\n")
        f.write(f"Failed [FAIL]: {failed}\n\n")
        for line in logs:
            f.write(line + '\n')

    print(f"Logs written to {log_path}")

def run_tests(test_dir, valid):
    logs = []

    all_files = []
    for root, _, files in os.walk(test_dir):
        all_files.extend(os.path.join(root, file) for file in files if file.endswith('.agu'))

    all_files.sort()

    for filepath in all_files:
        try:
            with open(filepath, 'r') as f:
                code = f.read()

        except Exception as e:
            logs.append(f"{filepath} [EXCEPTION]")
            logs.append(str(e))

        # Reset the parser (for the line counter)
        reset_parser()

        # Store stdout of parser
        output_buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_buffer):
                parser.parse(code, lexer=lexer)
            output = output_buffer.getvalue()
        except Exception as e:
            logs.append(f"{filepath} [EXCEPTION]")
            logs.append(str(e))

        if valid:
            if output.strip() == "":
                # No errors printed -> Test passed
                logs.append(f"{filepath} [✔]")
            else:
                # Expected no output, but got errors
                logs.append(f"{filepath} [FAIL]")
                logs.append(output)
        else:
            if output.strip() == "":
                # Expected errors, but got none
                logs.append(f"{filepath} [FAIL]")
                logs.append("Expected error but none found.")
            else:
                # Errors printed as expected
                logs.append(f"{filepath} [✔]")
                logs.append(output)

    return logs

def run_single_test(filepath):
    with open(filepath, 'r') as f:
        code = f.read()

    ast = parser.parse(code)
    print(ast)

def main():
    # If no args, accept stdin as program input
    if len(sys.argv) == 1:
        print("Write the AGUDA code to be parsed, followed by [ENTER] and Ctrl+D (EOF)")
        code = sys.stdin.read()
        ast = parser.parse(code)
        print("Parsed AST:")
        print("===================================")
        print(ast)
    
    elif len(sys.argv) == 2:
        # If the first argument is --tests, run all tests
        if sys.argv[1] == "--tests":
            invalid_sem_tests_logs = run_tests(INVALID_SEM_DIR, valid=False)
            write_logs(invalid_sem_tests_logs, "invalid-semantic-tests")

            invalid_syn_tests_logs = run_tests(INVALID_SYN_DIR, valid=False)
            write_logs(invalid_syn_tests_logs, "invalid-syntax-tests")

            valid_tests_logs = run_tests(VALID_DIR, valid=True)
            write_logs(valid_tests_logs, "valid-tests")
        
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