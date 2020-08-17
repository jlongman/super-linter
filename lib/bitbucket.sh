#!/usr/bin/env bash
BITBUCKET_CLONE_DIR=${BITBUCKET_CLONE_DIR}
BITBUCKET_COMMIT=${BITBUCKET_COMMIT}
BITBUCKET_REPO_OWNER=${BITBUCKET_REPO_OWNER}
BITBUCKET_REPO_SLUG=${BITBUCKET_REPO_SLUG}
VALIDATE_ALL_CODEBASE=${VALIDATE_ALL_CODEBASE}
OUTPUT_DETAILS="${OUTPUT_DETAILS:-detailed}"                   # What level of details. (simpler or detailed). Default simpler

DEFAULT_WORKSPACE="${DEFAULT_WORKSPACE-$BITBUCKET_CLONE_DIR}" # Default workspace if running locally
GITHUB_EVENT_PATH="${GITHUB_EVENT_PATH}"                      # Github Event Path
GITHUB_SHA="${BITBUCKET_COMMIT}"                              # GitHub sha from the commit
GITHUB_ORG="${BITBUCKET_REPO_OWNER}"                          # GitHub sha from the commit
GITHUB_REPO="${BITBUCKET_REPO_SLUG}"                          # GitHub sha from the commit
GITHUB_WORKSPACE="${BITBUCKET_CLONE_DIR}"                     # Github Workspace
DEFAULT_BRANCH="${DEFAULT_BRANCH:-$BITBUCKET_BRANCH}"         # Default Git Branch to use (master by default)
BITBUCKET_CODENOTIFY="${BITBUCKET_CODENOTIFY}"                # Boolean to enable bitbucket report api
DEFAULT_BITBUCKET_CODENOTIFY='false'                          # not bitbucket

GITHUB_EVENT_PATH=".github_event"
echo '{
  "repository":
  {
    "name": "'"${BITBUCKET_REPO_SLUG}"'",
    "owner": {
      "login": "'"${BITBUCKET_REPO_OWNER}"'"
    }
  }
  }' >${GITHUB_EVENT_PATH}

encodeComponentBB() {
  jq -aRs . <<<"$1"
}

bitbucket_report() {
  ERROR_COUNTER=$1
  if [[ "${VALIDATE_ALL_CODEBASE}" == "false" ]]; then
    message="This pull request introduces ${ERROR_COUNTER} lint problems."
  else
    message="This codebase contains ${ERROR_COUNTER} lint problems."
  fi
  if [[ "${ERROR_COUNTER}" -ne "0" ]]; then
    result="FAILED"
    safe="false"
  else
    result="PASSED"
    safe="true"
  fi
  curl \
    --proxy 'http://host.docker.internal:29418' \
    --request PUT \
    "http://api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_FULL_NAME}/commit/${BITBUCKET_COMMIT}/reports/superlint" \
    --header 'Content-Type: application/json' \
    --data-raw '{
	"title": "SuperLinter scan report",
	"details": "'"${message}"'",
	"report_type": "BUG",
	"reporter": "superlint",
	"result": "'"${result}"'",
	"data": [
		{
			"title": "Safe to merge?",
			"type": "BOOLEAN",
			"value": '"${safe}"'
		}
	]
}'
}

bitbucket_annotate() {
  DETAILS=$(encodeComponentBB "${LINT_CMD}" | sed -e 's|\n|<br />\n|g') # note already quoted
  data='{
    "title": "'"${LINTER_NAME} - ${TOTAL_ERRORS_FOUND}/${#LIST_FILES[@]} - ${FILE_TYPE}"'",
    "summary": "'"${LINTER_NAME}"' detected a problem",
    "details": '"${DETAILS}"',
    "annotation_type": "CODE_SMELL",
    "reporter": "superlint",
    "path": "'"${FILE}"'",
    "data": [
      {
        "title": "Safe to merge?",
        "type": "BOOLEAN",
        "value": false
      }
    ]
  }'
  #          echo "$data"                      #FIXME
  #          echo "totes: $TOTAL_ERRORS_FOUND" # FIXME

  curl \
    --proxy 'http://host.docker.internal:29418' \
    --request PUT \
    "http://api.bitbucket.org/2.0/repositories/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}/commit/${BITBUCKET_COMMIT}/reports/superlint/annotations/$TOTAL_ERRORS_FOUND" \
    --header 'Content-Type: application/json' \
    --data-raw "${data}"
}
################
##########################
# Get the run local flag #
##########################
if [ -z "$BITBUCKET_CODENOTIFY" ]; then
  ##################################
  # No flag passed, set to default #
  ##################################
  BITBUCKET_CODENOTIFY="$DEFAULT_BITBUCKET_CODENOTIFY"
fi

###############################
# Convert string to lowercase #
###############################
BITBUCKET_CODENOTIFY=$(echo "$BITBUCKET_CODENOTIFY" | awk '{print tolower($0)}')

# we need default_run_local applied
if [[ "$RUN_LOCAL" == "false" && "$BITBUCKET_CODENOTIFY" != "false" ]]; then
  bitbucket_report 0
fi
