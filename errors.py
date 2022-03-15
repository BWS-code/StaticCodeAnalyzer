import re


def check_s001(line: str, line_ind: int, lines: list, max_length=79) -> str | None:
    if len(line) > max_length:
        return f'Line {line_ind + 1}: S001 Too long'
    return None

def check_s002(line: str, line_ind: int, lines: list, multiple=4) -> str | None:
    indent = len(line) - len(line.lstrip())
    if line != '\n' and indent % multiple:
        return f'Line {line_ind + 1}: S002 Indentation is not a multiple of four'
    return None

def check_s003(line: str, line_ind: int, lines: list) -> str | None:
    if ';' in line:
        line_ch = [ch for ch in line if ch in ('"', "'", '#', ';')]
        is_in_string = True if (line_ch[line_ch.index(';') + 1:].count("'") +
                                line_ch[line_ch.index(';') + 1:].count('"')) % 2 else False
        is_in_comment = True if '#' in line_ch[:line_ch.index(';') + 1] and not is_in_string else False
        if not is_in_string and not is_in_comment:
            return f'Line {line_ind + 1}: S003 Unnecessary semicolon'
        return None

def check_s004(line: str, line_ind: int, lines: list) -> str | None:
    if '#' in line and line.index('#') > 1 and not re.match(r'.+\s{2,}#.*', line):
        return f'Line {line_ind + 1}: S004 At least two spaces required before inline comments'
    return None

def check_s005(line: str, line_ind: int, lines: list) -> str | None:
    if '#' in line and re.match(r'.*todo.*', line[line.index('#') + 1:], flags=re.I):
        return f'Line {line_ind + 1}: S005 TODO found'
    return None

def check_s006(line: str, line_ind: int, lines: list) -> str | None:
    if line_ind > 2 and all(['blank' if lines[line_ind - i] == '\n' else '' for i in range(1, 4)]):
        return f'Line {line_ind + 1}: S006 More than two blank lines used before this line'
    return None


errors_dict = {
    'S001': 'Too long',
    'S002': 'Indentation is not a multiple of four',
    'S003': 'Unnecessary semicolon',
    'S004': 'At least two spaces required before inline comments',
    'S005': 'TODO found',
    'S006': 'More than two blank lines used before this line'
}
