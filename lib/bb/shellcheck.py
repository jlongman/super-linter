from . import lint2bb_parser


class Parser(lint2bb_parser):
    def __init__(self, linter, file_type, file):
        lint2bb_parser.__init__(self, linter, file_type, file)

    def parse(self, messages):
        errors = []
        last_message = None
        last_summary = None
        raw_line = messages.readline()
        line = -1  # error case
        import sys  # fixme remove sys w/ debugging
        while raw_line != "":
            raw_line = raw_line.strip()
            print(raw_line, file=sys.stderr)
            if raw_line == "":
                raw_line = messages.readline()
                continue
            if raw_line.startswith("In "):
                if last_message is not None:
                    errors.append({
                        "parser": self.linter,
                        "fileType": self.file_type,
                        "file": self.file,
                        "line": int(line),
                        "level": "warning",
                        "message": last_message,
                        "summary": last_summary,
                    })
                last_message = ""
                last_summary = None
                line_offset = raw_line.index(" line ") + len(" line ")
                line = raw_line[line_offset:-1]
            else:
                if raw_line.startswith("^-- "):
                    last_summary = raw_line[len("^-- "):]
                last_message = f"{last_message} {raw_line}"
            raw_line = messages.readline()

        if last_message is not None:
            errors.append({
                "parser": self.linter,
                "fileType": self.file_type,
                "file": self.file,
                "line": int(line),
                "level": "MEDIUM",
                "severity": "MEDIUM",
                "message": last_message,
            })

        return errors
