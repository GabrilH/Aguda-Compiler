class ErrorLogger:
    def __init__(self, max_errors, error_type):
        self.max_errors = max_errors
        self.messages = []
        self.error_type = error_type

    def log(self, message: str, lineno: int, column: int):
        self.messages.append(f"{self.error_type} Error: ({lineno}, {column}) {message}")

    def print_errors(self):
        for error in self.messages[:self.max_errors]:
            print(error)
        if len(self.messages) > self.max_errors:
            print(f"...and {len(self.messages) - self.max_errors} more errors.")

    def has_errors(self) -> bool:
        return len(self.messages) > 0

    def reset(self):
        self.messages = []

    def get_errors(self):
        return self.messages