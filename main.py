from errors_handler import *
from pathlib import Path
from sys import argv


class CodeAnalyzer:
    def __init__(self, base_path: str, error_map: dict[str, str],
                 check_initials: list, checks: int, formatting: int = 2):
        self.base_path = base_path
        self.error_map = error_map
        self.lines = None
        self.errors_results = None
        self.check_initials = check_initials
        self.checks = checks + 1
        self.formatting = formatting

    def open_file(self, path: str) -> None:
        with open(path, 'r') as file:
            self.lines = [line for line in file.readlines()]

    def run_checks(self, letter: str, qty: int) -> None:
        checks = [''.join((f'check_{letter}00', str(i), '(line, line_ind, self.lines)')) for i in range(1, qty)]
        self.errors_results = []
        for line in self.lines:
            line_ind = self.lines.index(line)
            for check in checks:
                if eval(check) and eval(check) not in self.errors_results:
                    self.errors_results.append(eval(check))

    def print_errs(self, path: str) -> None:
        if self.errors_results:
            if self.formatting == 2:
                print(path)
            for err in self.errors_results:
                if self.formatting == 1:
                    print(path, end=': ')
                print(err)

    def get_files(self) -> list:
        if str(self.base_path).endswith('.py'):
            return [self.base_path]
        folders = [self.base_path] + [entry for entry in self.base_path.iterdir() if entry.is_dir()]
        files = [entry for path in folders for entry in path.iterdir() if
                 entry.is_file() and entry.name.endswith('.py')]
        return files

    def analyze(self) -> None:
        for path in self.get_files():
            self.open_file(path)
            for letter in self.check_initials:
                self.run_checks(letter, self.checks)
            self.print_errs(path)


args = argv
user_path = Path(args[1])
check_letters = ['s']

my_analyzer = CodeAnalyzer(user_path, errors_dict,
                           check_letters, checks=9,
                           formatting=1)

if __name__ == '__main__':
    my_analyzer.analyze()
