import os
import sys
import datetime
from lexer import lexer
from parser import parser

def run_invalid_tests(invalid_dir):
    log = ["Invalid Aguda Programs\n"]
    for root, _, files in os.walk(invalid_dir):
        for file in files:
            if file.endswith(".agu"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        code = f.read()
                    parser.parse(code, lexer=lexer)
                    # Parsed successfully -> should fail
                    log.append(f"{filepath} [FAIL]")
                except Exception:
                    # Parsing failed as expected
                    log.append(f"{filepath} [✔]")
    return log


def run_valid_tests(valid_dir):
    failures = []
    for root, _, files in os.walk(valid_dir):
        for file in files:
            if file.endswith(".agu"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        code = f.read()
                    parser.parse(code, lexer=lexer)
                    # Parsed successfully
                except Exception as e:
                    failures.append((filepath, str(e)))
    return failures


def write_logs(invalid_log, valid_failures):
    today = datetime.date.today().isoformat()
    # Invalid log
    with open(f'invalid-{today}.log', 'w') as f:
        for line in invalid_log:
            f.write(line + '\n')

    # Valid log
    with open(f'valid-{today}.log', 'w') as f:
        if not valid_failures:
            f.write("All valid programs passed!\n")
            return
        f.write("Failures:\n\n")
        for filepath, error in valid_failures:
            f.write(f"{filepath}\n")
            f.write(f"  {error}\n\n")


def main():
    invalid_log = run_invalid_tests('test/invalid')
    valid_failures = run_valid_tests('test/valid')
    write_logs(invalid_log, valid_failures)
    print("Testing completed. Logs generated.")

if __name__ == '__main__':
    main()
