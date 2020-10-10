#!/usr/bin/env bash
CODEBUILD_SRC_DIR=${CODEBUILD_SRC_DIR}
#CODEBUILD_COMMIT=${CODEBUILD_COMMIT}
#CODEBUILD_REPO_OWNER=${CODEBUILD_REPO_OWNER}
#CODEBUILD_REPO_SLUG=${CODEBUILD_REPO_SLUG}
VALIDATE_ALL_CODEBASE=${VALIDATE_ALL_CODEBASE}
OUTPUT_DETAILS="${OUTPUT_DETAILS:-detailed}" # What level of details. (simpler or detailed). Default simpler
MULTI_STATUS='false'
DEFAULT_WORKSPACE="${DEFAULT_WORKSPACE-$CODEBUILD_SRC_DIR}" # Default workspace if running locally
GITHUB_EVENT_PATH="${GITHUB_EVENT_PATH}"                    # Github Event Path
#GITHUB_SHA="${CODEBUILD_COMMIT}"                              # GitHub sha from the commit
#GITHUB_ORG="${CODEBUILD_REPO_OWNER}"                          # GitHub sha from the commit
#GITHUB_REPO="${CODEBUILD_REPO_SLUG}"                          # GitHub sha from the commit
#GITHUB_WORKSPACE="${CODEBUILD_CLONE_DIR}"                     # Github Workspace
#DEFAULT_BRANCH="${DEFAULT_BRANCH:-$CODEBUILD_BRANCH}"         # Default Git Branch to use (master by default)
#CODEBUILD_CODENOTIFY="${CODEBUILD_CODENOTIFY}"                # Boolean to enable CODEBUILD report api
#DEFAULT_CODEBUILD_CODENOTIFY='false'                          # not CODEBUILD

GITHUB_EVENT_PATH=".github_event"
echo '{
  "repository":
  {
    "name": "'"${CODEBUILD_REPO_SLUG}"'",
    "owner": {
      "login": "'"${CODEBUILD_REPO_OWNER}"'"
    }
  }
  }' >${GITHUB_EVENT_PATH}

encodeComponentBB() {
  jq -aRs . <<<"$1"
}
