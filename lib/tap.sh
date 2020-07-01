#!/usr/bin/env bash
##############
# Format     #
##############
DEFAULT_WORKSPACE="${DEFAULT_WORKSPACE}"
OUTPUT_FORMAT="${OUTPUT_FORMAT}"                      # Output format to be generated. Default none
OUTPUT_FOLDER="${OUTPUT_FOLDER:-super-linter.report}" # Folder where the reports are generated. Default super-linter.report
OUTPUT_DETAILS="${OUTPUT_DETAILS:-detailed}" # Folder where the reports are generated. Default super-linter.report
REPORT_OUTPUT_FOLDER="${DEFAULT_WORKSPACE}/${OUTPUT_FOLDER}"
XUNIT_OUTPUT_FOLDER="${DEFAULT_WORKSPACE}/${OUTPUT_FOLDER}/test-reports"


################################################################################
#### Function IsTap ############################################################
IsTAP() {
  if [[ "${OUTPUT_FORMAT}" == "tap" ]] || [[ "${OUTPUT_FORMAT}" == "xunit" ]]; then
    return 0
  else
    return 1
  fi
}
################################################################################
#### Function IsXUnit ############################################################
IsXUNIT() {
  if [[ "${OUTPUT_FORMAT}" == "xunit" ]]; then
    return 0
  else
    return 1
  fi
}

if IsTAP; then
    encodeComponent() {
      jq -aRs . <<<"$1"
    }

    TransformTAPDetails()
    {
      DATA=$1
      if [ -n "${DATA}" ] && [ "${OUTPUT_DETAILS}" == "detailed" ] ; then
        #########################################################
        # Transform new lines to \\n, remove colours and colons #
        #########################################################
        echo "${DATA}" | awk 'BEGIN{RS="\n";ORS="\\n"}1' | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g" | tr ':' ' '
      fi
    }

    ##############################################################
    # check flag for validating the report folder does not exist #
    ##############################################################
    if [[ -d "${REPORT_OUTPUT_FOLDER}" ]]; then
        echo "ERROR! Found ${REPORT_OUTPUT_FOLDER}"
        echo "Please remove the folder and try again."
        exit 1
    fi

    mkdir -p "${XUNIT_OUTPUT_FOLDER}" # FIXME
fi