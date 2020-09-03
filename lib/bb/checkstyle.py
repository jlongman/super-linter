from . import stdlint


# Starting audit...
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:1: Missing package-info.java file. [JavadocPackage]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:4:5: Missing a Javadoc comment. [JavadocVariable]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:6:5: Class 'AppVersion' looks like designed for extension (can be subclassed), but the method 'getVersion' does not have javadoc that explains how to do that safely. If class is not designed for extension consider making the class 'AppVersion' final or making the method 'getVersion' static/final/abstract/empty, or adding allowed annotation for the method. [DesignForExtension]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:6:5: Missing a Javadoc comment. [MissingJavadocMethod]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:10:5: Class 'AppVersion' looks like designed for extension (can be subclassed), but the method 'setVersion' does not have javadoc that explains how to do that safely. If class is not designed for extension consider making the class 'AppVersion' final or making the method 'setVersion' static/final/abstract/empty, or adding allowed annotation for the method. [DesignForExtension]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:10:5: Missing a Javadoc comment. [MissingJavadocMethod]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:10:28: Parameter version should be final. [FinalParameters]
# [ERROR] /opt/atlassian/pipelines/agent/build/backend/framework/spring-rxjava/src/main/java/com/protmv/takeover/common/AppVersion.java:10:35: 'version' hides a field. [HiddenField]
# Audit done.
# Checkstyle ends with 8 errors.


class Parser(stdlint.Parser):
    def __init__(self, linter, file_type, file):
        stdlint.Parser.__init__(self, linter, file_type, file)

    def process_line(self, raw_line):
        if raw_line.startswith('Starting audit...'):
            return None
        elif raw_line.startswith('Audit done.'):
            return None
        elif raw_line.startswith('Checkstyle ends with '):
            return None
        return super().process_line(raw_line[len("[ERROR] "):])


if __name__ == "__main__":
    # run doctest by running : `python3 -m lib.bb.checkstyle`
    import doctest

    doctest.testfile("checkstyle.doctest")
