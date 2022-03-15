import re
from errors import errors_dict
from pathlib import Path
from sys import argv


class CodeAnalyzer:
    def __init__(self, base_path: str, error_map: dict[str, str]):
        self.base_path = base_path
        self.error_map = error_map
        self.lines = None
        self.errors_results = None

    def open_file(self, path: str) -> None:
        with open(path, 'r') as file:
            self.lines = [line for line in file.readlines()]

    def run_checks(self, letter: str, qty: int) -> None:
        checks = [''.join((f'self.check_{letter}00', str(i), '(line, line_ind)')) for i in range(1, qty)]
        self.errors_results = []
        for line in self.lines:
            line_ind = self.lines.index(line)
            for check in checks:
                if eval(check) and eval(check) not in self.errors_results:
                    self.errors_results.append(eval(check))

    def check_s001(self, line: str, line_ind: int, max_length=79) -> str | None:
        if len(line) > max_length:
            return f'Line {line_ind + 1}: S001 Too long'
        return None

    def check_s002(self, line: str, line_ind: int, multiple=4) -> str | None:
        indent = len(line) - len(line.lstrip())
        if line != '\n' and indent % multiple:
            return f'Line {line_ind + 1}: S002 Indentation is not a multiple of four'
        return None

    def check_s003(self, line: str, line_ind: int) -> str | None:
        if ';' in line:
            line_ch = [ch for ch in line if ch in ('"', "'", '#', ';')]
            is_in_string = True if (line_ch[line_ch.index(';') + 1:].count("'") +
                                    line_ch[line_ch.index(';') + 1:].count('"')) % 2 else False
            is_in_comment = True if '#' in line_ch[:line_ch.index(';') + 1] and not is_in_string else False
            if not is_in_string and not is_in_comment:
                return f'Line {line_ind + 1}: S003 Unnecessary semicolon'
            return None

    def check_s004(self, line: str, line_ind: int) -> str | None:
        if '#' in line and line.index('#') > 1 and not re.match(r'.+\s{2,}#.*', line):
            return f'Line {line_ind + 1}: S004 At least two spaces required before inline comments'
        return None

    def check_s005(self, line: str, line_ind: int) -> str | None:
        if '#' in line and re.match(r'.*todo.*', line[line.index('#') + 1:], flags=re.I):
            return f'Line {line_ind + 1}: S005 TODO found'
        return None

    def check_s006(self, line: str, line_ind: int) -> str | None:
        if line_ind > 2 and all(['blank' if self.lines[line_ind - i] == '\n' else '' for i in range(1, 4)]):
            return f'Line {line_ind + 1}: S006 More than two blank lines used before this line'
        return None

    def print_errs(self, path: str) -> None:
        if self.errors_results:
            for err in self.errors_results:
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
            self.run_checks('s', 7)
            self.print_errs(path)


args = argv
user_path = Path(args[1])
my_analyzer = CodeAnalyzer(user_path, errors_dict)

if __name__ == '__main__':
    my_analyzer.analyze()
