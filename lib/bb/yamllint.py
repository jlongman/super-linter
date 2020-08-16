from . import lint2bb_parser


# docker run -v $PWD/./config/dev/base:/tmp/lint -e RUN_LOCAL=true -eVALIDATE_YML=true  --rm -it jlongman/super-linter:stable
# ERROR:[/tmp/lint/config/dev/base/bastion.yaml
#   1:1       warning  missing document start "---"  (document-start)
#   9:18      warning  too many spaces inside braces  (braces)
#   9:49      warning  too many spaces inside braces  (braces)
#   11:17     warning  too many spaces inside braces  (braces)
#   11:39     warning  too many spaces inside braces  (braces)

# lookup table
levels = {
    "warning": "MEDIUM",
    "error": "HIGH"
}


def get_level(level):
    try:
        return levels[level]
    except:
        return "HIGH"


class Parser(lint2bb_parser):
    def __init__(self, linter, file_type, file):
        lint2bb_parser.__init__(self, linter, file_type, file)

    def parse(self, messages):
        errors = []
        raw_line = messages.readline()
        if raw_line.strip() is self.file:
            # dedup
            raw_line = messages.readline()
        import sys
        while raw_line != "":
            raw_line = raw_line.strip()
            print(raw_line, file=sys.stderr)
            if raw_line == "":
                raw_line = messages.readline()
                continue
            parse_line = raw_line.split(None, 2)
            if len(parse_line) >= 3:
                # print(parse_line)
                line, column = parse_line[0].split(':')
                level = parse_line[1]
                message = parse_line[2]
                errors.append({
                    "parser": self.linter,
                    "fileType": self.file_type,
                    "file": self.file,
                    "line": int(line),
                    "column": int(column),
                    "level": level,
                    "message": message,
                    "summary": message,
                    "severity": get_level(level)
                })
            # else:
            #     print(parse_line)
            #     print(raw_line)
            raw_line = messages.readline()

        return errors
