class CodeAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines = None
        self.errors = None

    def open_file(self) -> None:
        with open(self.filepath, 'r') as file:
            self.lines = [line for line in file.readlines()]

    def check_length(self, max_length=79) -> None:
        self.errors = [f'Line {line_num + 1}: S001 Too long' for line_num, line in
                       enumerate(self.lines) if len(line) > max_length]

    def print_errs(self) -> None:
        if self.errors:
            print('\n'.join(self.errors))

    def analyze(self) -> None:
        self.open_file()
        self.check_length()
        self.print_errs()

filename = input()
my_analyzer = CodeAnalyzer(filename)

if __name__ == '__main__':
    my_analyzer.analyze()
