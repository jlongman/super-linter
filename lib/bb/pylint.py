from . import stdlint

# note "***** Module" should be skipped by stdlint try catch

# docker run -v $PWD/./scripts/plat-5:/tmp/lint -e RUN_LOCAL=true -eVALIDATE_PYTHON_PYLINT=true  \
#       --rm -it jlongman/super-linter:stable
# 2020-08-16 19:53:50 [ERROR ]   [************* Module redis-snapshot-export
# scripts/plat-5/redis-snapshot-export.py:6:0: E0401: Unable to import 'tmvawslib' (import-error)
# scripts/plat-5/redis-snapshot-export.py:7:0: E0401: Unable to import 'waiter' (import-error)
# scripts/plat-5/redis-snapshot-export.py:86:4: E1120: No value for argument 'instance_name' in \
#   function call (no-value-for-parameter)
# scripts/plat-5/redis-snapshot-export.py:86:4: E1120: No value for argument 'jira_issue' in \
#   function call (no-value-for-parameter)]


class Parser(stdlint.Parser):
    def __init__(self, linter, file_type, file):
        stdlint.Parser.__init__(self, linter, file_type, file)
