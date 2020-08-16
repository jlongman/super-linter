from . import lint2bb_parser
import pprint
# /tmp/lint/README.md:15:23 MD009/no-trailing-spaces Trailing spaces [Expected: 0 or 2; Actual: 1]
# /tmp/lint/README.md:26:43 MD009/no-trailing-spaces Trailing spaces [Expected: 0 or 2; Actual: 1]
# /tmp/lint/README.md:29:42 MD009/no-trailing-spaces Trailing spaces [Expected: 0 or 2; Actual: 1]


class Parser(lint2bb_parser):

    def __init__(self, linter, file_type, file):
        lint2bb_parser.__init__(self, linter, file_type, file)

    def parse(self, messages):
        errors = []
        raw_line = messages.readline()
        # if raw_line.strip() is self.file:
        #     # dedup
        #     raw_line = messages.readline()
        import sys
        while raw_line != "":
            try:
                raw_line = raw_line.strip()
                print(raw_line, file=sys.stderr)
                file, line, parse_line = raw_line.split(':', 2)
                column, message = parse_line.split(' ', 1)
                errors.append({
                    "parser": self.linter,
                    "fileType": self.file_type,
                    "file": self.file,
                    "line": int(line),
                    "column": int(column),
                    "level": "HIGH",
                    "message": message,
                    "severity": "HIGH"
                })
                # else:
                #     print(parse_line)
                #     print(raw_line)
                raw_line = messages.readline()
            except Exception as e:
                pprint.pprint(e, stream=sys.stderr)
        return errors
