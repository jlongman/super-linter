from . import lint2bb_parser


class Parser(lint2bb_parser):
    def __init__(self, linter, file_type, file):
        lint2bb_parser.__init__(self, linter, file_type, file)

    def parse(self, messages):
        errors = []
        last_message = None
        raw_line = messages.readline()
        line = -1 # error case
        while raw_line != "":
            if raw_line.startswith("In "):
                if last_message is not None:
                    errors.append({
                        "parser": self.linter,
                        "fileType": self.file_type,
                        "file": self.file,
                        "line": line,
                        "level": "warning",
                        "message": last_message,
                    })
                last_message = ""
                line_offset = raw_line.index(" line ") + len(" line ")
                line = raw_line[line_offset:-1]
            else:
                last_message = f"{last_message} {raw_line}"
            raw_line = messages.readline()

        if last_message is not None:
            errors.append({
                "parser": self.linter,
                "fileType": self.file_type,
                "file": self.file,
                "line": line,
                "level": "MEDIUM",
                "severity": "MEDIUM",
                "message": last_message,
            })

        return errors
