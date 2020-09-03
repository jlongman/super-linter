from . import stdlint


class Parser(stdlint.Parser):
    def __init__(self, linter, file_type, file):
        stdlint.Parser.__init__(self, linter, file_type, file)

    def process_line(self, raw_line):
        if raw_line.startswith('standard: Use JavaScript Standard Style'):
            return None
        elif raw_line.startswith('standard: Run `standard --fix` to automatically fix some problems.'):
            return None
        return super().process_line(raw_line)


if __name__ == "__main__":
    # run doctest by running : `python3 -m lib.bb.standard`
    import doctest
    doctest.testfile("standard.doctest")
