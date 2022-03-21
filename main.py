from errors_handler import *
from pathlib import Path
import sys
import ast



class CodeAnalyzer:
    def __init__(self,
                 base_path: str,
                 check_initials: list,
                 formatting: int = 2):
        self.base_path = base_path
        self.tree = None
        self.lines = None
        self.errors_results = None
        self.check_initials = check_initials
        self.formatting = formatting

    def open_file(self, path: str) -> None:
        with open(path, 'r') as file:
            self.lines = [line for line in file.readlines()]
        with open(path, 'r') as file:
            self.tree = ast.parse(file.read())


    def run_checks1(self, letter: str) -> None:
        checks = [''.join((f'check_{letter}00', str(i), '(line, line_ind, self.lines)')) for i in range(1, 10)]
        for line in self.lines:
            line_ind = self.lines.index(line)
            for check in checks:
                if eval(check) and eval(check) not in self.errors_results:
                    self.errors_results.append(eval(check))

    def run_checks2(self, letter: str) -> None:
        checks = [''.join((f'check_{letter}0', str(i), '(self.tree)')) for i in range(10, 13)]
        for check in checks:
            if eval(check) and eval(check) not in self.errors_results:
                self.errors_results += eval(check)

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
            self.errors_results = []
            self.open_file(path)
            for letter in self.check_initials:
                self.run_checks1(letter)
                self.run_checks2(letter)
            self.print_errs(path)


args = sys.argv
check_letters = ['s']

if __name__ == '__main__':
    user_path = Path(input('Enter path to dir or file >')) if len(args) == 1 else Path(args[1])
    my_analyzer = CodeAnalyzer(user_path, check_letters, formatting=1)
    my_analyzer.analyze() 
