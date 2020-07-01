###########################################
###########################################
## Dockerfile to run GitHub Super-Linter ##
###########################################
###########################################

##################
# Get base image #
##################
FROM github/super-linter:v3.1.1
RUN npm -g --no-cache install \
    tap-xunit@2.4.1 && \
    pip install --no-cache-dir \
    boto3 \
    click \
    troposphere

###########################################
# Load GitHub Env Vars for GitHub Actions #
###########################################
ENV GITHUB_SHA=${GITHUB_SHA} \
    GITHUB_EVENT_PATH=${GITHUB_EVENT_PATH} \
    GITHUB_WORKSPACE=${GITHUB_WORKSPACE} \
    DEFAULT_BRANCH=${DEFAULT_BRANCH} \
    VALIDATE_ALL_CODEBASE=${VALIDATE_ALL_CODEBASE} \
    LINTER_RULES_PATH=${LINTER_RULES_PATH} \
    VALIDATE_YAML=${VALIDATE_YAML} \
    VALIDATE_JSON=${VALIDATE_JSON} \
    VALIDATE_XML=${VALIDATE_XML} \
    VALIDATE_MD=${VALIDATE_MD} \
    VALIDATE_BASH=${VALIDATE_BASH} \
    VALIDATE_PERL=${VALIDATE_PERL} \
    VALIDATE_PHP=${VALIDATE_PHP} \
    VALIDATE_PYTHON=${VALIDATE_PYTHON} \
    VALIDATE_RUBY=${VALIDATE_RUBY} \
    VALIDATE_COFFEE=${VALIDATE_COFFEE} \
    VALIDATE_ANSIBLE=${VALIDATE_ANSIBLE} \
    VALIDATE_DOCKER=${VALIDATE_DOCKER} \
    VALIDATE_JAVASCRIPT_ES=${VALIDATE_JAVASCRIPT_ES} \
    VALIDATE_JAVASCRIPT_STANDARD=${VALIDATE_JAVASCRIPT_STANDARD} \
    VALIDATE_TYPESCRIPT_ES=${VALIDATE_TYPESCRIPT_ES} \
    VALIDATE_TYPESCRIPT_STANDARD=${VALIDATE_TYPESCRIPT_STANDARD} \
    VALIDATE_GO=${VALIDATE_GO} \
    VALIDATE_TERRAFORM=${VALIDATE_TERRAFORM} \
    VALIDATE_CSS=${VALIDATE_CSS} \
    VALIDATE_ENV=${VALIDATE_ENV} \
    VALIDATE_CLOJURE=${VALIDATE_CLOJURE} \
    VALIDATE_KOTLIN=${VALIDATE_KOTLIN} \
    VALIDATE_POWERSHELL=${VALIDATE_POWERSHELL} \
    VALIDATE_OPENAPI=${VALIDATE_OPENAPI} \
    VALIDATE_PROTOBUF=${VALIDATE_PROTOBUF} \
    ANSIBLE_DIRECTORY=${ANSIBLE_DIRECTORY} \
    RUN_LOCAL=${RUN_LOCAL} \
    TEST_CASE_RUN=${TEST_CASE_RUN} \
    ACTIONS_RUNNER_DEBUG=${ACTIONS_RUNNER_DEBUG} \
    DISABLE_ERRORS=${DISABLE_ERRORS}
ENV THIS_SSH_KEY=${THIS_SSH_KEY}\
    OUTPUT_FORMAT=${OUTPUT_FORMAT} \
    OUTPUT_FOLDER=${OUTPUT_FOLDER} \
    BITBUCKET_CODENOTIFY=${BITBUCKET_CODENOTIFY}

#############################
# Copy scripts to container #
#############################
COPY lib /action/lib

##################################
# Copy linter rules to container #
##################################
COPY TEMPLATES /action/lib/.automation

######################
# Set the entrypoint #
######################
ENTRYPOINT ["/action/lib/linter.sh"]
