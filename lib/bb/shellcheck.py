from . import lint2bb_parser
# from __init__ import lint2bb_parser  # required for doctest, replace above

ERROR_LEVEL = "MEDIUM"


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
            # print(raw_line, file=sys.stderr)
            if raw_line == "":
                raw_line = messages.readline()
                continue
            if raw_line.startswith("In "):
                if last_message is not None:
                    event = self.to_event(last_message, last_summary, line)
                    errors.append(event)
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
            event = self.to_event(last_message, last_summary, line)
            errors.append(event)

        return errors

    def to_event(self, last_message, summary, line):
        event = {
            "parser": self.linter,
            "fileType": self.file_type,
            "file": self.file,
            "line": int(line),
            "level": ERROR_LEVEL,
            "severity": ERROR_LEVEL,
            "message": last_message,
        }
        if summary is not None:
            event["summary"] = summary
        return event


if __name__ == "__main__":
    import doctest

    doctest.testfile("shellcheck.doctest")
