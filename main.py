import re
from errors import errors_dict


class CodeAnalyzer:
    def __init__(self, filepath: str, error_map: dict[str, str]):
        self.filepath = filepath
        self.error_map = error_map
        self.lines = None
        self.errors_results = []

    def open_file(self) -> None:
        with open(self.filepath, 'r') as file:
            self.lines = [line for line in file.readlines()]

    def run_checks(self, letter: str, qty: int) -> None:
        checks = [''.join((f'self.check_{letter}00', str(i), '(line, line_ind)')) for i in range(1, qty)]
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
            is_in_string = True if (line[line.index(';') + 1:].count("'") +
                                    line[line.index(';') + 1:].count('"')) % 2 else False
            is_in_comment = True if '#' in line[:line.index(';') + 1] and not is_in_string else False
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

    def print_errs(self) -> None:
        if self.errors_results:
            print('\n'.join(self.errors_results))

    def analyze(self) -> None:
        self.open_file()
        self.run_checks('s', 7)
        self.print_errs()

filename = input()
my_analyzer = CodeAnalyzer(filename, errors_dict)

if __name__ == '__main__':
    my_analyzer.analyze()
