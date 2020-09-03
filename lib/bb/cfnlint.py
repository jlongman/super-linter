from . import lint2bb_parser
# from __init__ import lint2bb_parser  # required for doctest, replace above

ERROR_LEVEL = "MEDIUM"


# docker run -v $PWD/./cloudformation/templates/yaml/prod:/tmp/lint -e RUN_LOCAL=true
#    -eVALIDATE_CLOUDFORMATION=true  --rm -it jlongman/super-linter:stable
# 2020-08-17 00:55:36 [ERROR ]   [W1001 Ref to resource "AdminScale" that may not be available when condition "IsProd" is False at Outputs/AdminAutoScalingGroup/Value/Ref
# /tmp/lint/cloudformation/templates/yaml/prod/90.manyvids-app-prod.cf.yaml:44:5
#
# W3005 Obsolete DependsOn on resource (MvWebAccessSG), dependency already enforced by a "Ref" at Resources/MvInternalSG/Properties/SecurityGroupIngress/0/SourceSecurityGroupId/Ref
# /tmp/lint/cloudformation/templates/yaml/prod/90.manyvids-app-prod.cf.yaml:123:5

class Parser(lint2bb_parser):
    def __init__(self, linter, file_type, file):
        lint2bb_parser.__init__(self, linter, file_type, file)

    def parse(self, messages):
        errors = []
        raw_line = messages.readline()
        line = -1  # error case
        while raw_line != "":
            raw_line = raw_line.strip()
            # print(raw_line, file=sys.stderr)
            if raw_line == "":
                raw_line = messages.readline()
                continue
            rcolumn, rline, rmessage = raw_line[::-1].split(':', 2)
            message = rmessage[::-1]
            column = rcolumn[::-1]
            line = rline[::-1]
            event = self.to_event(message, None, line, column)
            errors.append(event)
            raw_line = messages.readline()

        return errors

    def to_event(self, last_message, summary, line, column):
        event = {
            "parser": self.linter,
            "fileType": self.file_type,
            "file": self.file,
            "line": int(line),
            "column": int(column),
            "level": ERROR_LEVEL,
            "severity": ERROR_LEVEL,
            "message": last_message,
        }
        if summary is not None:
            event["summary"] = summary
        return event


if __name__ == "__main__":
    import doctest

    doctest.testfile("cfnlint.doctest")
