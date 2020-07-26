#!/usr/bin/env python3
import sys
import importlib
import requests
import os
import json
import pprint

repo_owner = os.getenv("BITBUCKET_REPO_OWNER")
repo_slug = os.getenv("BITBUCKET_REPO_SLUG")
bitbucket_commit = os.getenv("BITBUCKET_COMMIT")

report_url = "http://api.bitbucket.org/2.0/repositories/{}/{}/commit/{}/reports/superlint".format(
    repo_owner,
    repo_slug,
    bitbucket_commit,
)
headers = {
    'content-type': 'application/json'
}
proxies = {
    "http": 'http://host.docker.internal:29418',
    "https": 'http://host.docker.internal:29418'
}


def report(this_count, data):
    document = {
        'title': 'SuperLinter scan report {}'.format(this_count),
        'report_type': 'BUG',
        'reporter': linter,
        'result': '{result}'.format(result=data["result"]),
        'data': [{
            'title': 'Safe to merge?',
            'type': 'BOOLEAN',
            'value': data["safe"]
        }],
        'summary': '{linter} detected a problem'.format(linter=linter),
        'details': data["message"],
    }
    r = requests.put(
        url=report_url,
        proxies=proxies,
        headers=headers,
        data=json.dumps(document)
    )
    if r.status_code != 200:
        print(json.dumps(document), file=sys.stderr)
        pprint.pprint(r, stream=sys.stderr)
        pprint.pprint(r.text, stream=sys.stderr)


def annotate_single(this_count, data):
    document = get_annotation_document(data, this_count)
    annotation_url = report_url + "/annotations/{}".format(
        this_count
    )

    r = requests.put(
        url=annotation_url,
        proxies=proxies,
        headers=headers,
        data=json.dumps(document)
    )
    if r.status_code != 200:
        print(json.dumps(document), file=sys.stderr)
        pprint.pprint(r, stream=sys.stderr)
        pprint.pprint(r.text, stream=sys.stderr)


def annotate_batch(this_count, data):
    annotations = []
    for single_result in data:
        annotations.append(get_annotation_document(single_result, this_count))
        this_count += 1

    group_annotation_url = report_url + "/annotations"
    r = requests.post(
        url=group_annotation_url,
        proxies=proxies,
        headers=headers,
        data=json.dumps(annotations)
    )
    if r.status_code != 200:
        print(json.dumps(annotations), file=sys.stderr)
        pprint.pprint(r, stream=sys.stderr)
        pprint.pprint(r.text, stream=sys.stderr)


def get_annotation_document(data, this_count):
    document = {
        'external_id': 'super-{linter}-{filetype}-{count}'.format(linter=linter, filetype=file_type, count=this_count),
        'title': '{linter} - {filetype}'.format(linter=linter, filetype=file_type),
        'summary': 'Super-linter/{linter} detected problem # {count}'.format(linter=linter, count=this_count),
        'details': data["message"],
        'annotation_type': 'CODE_SMELL',
        'reporter': 'superlint',
        'path': data['file']
    }
    if 'line' in data:
        document['line'] = data['line']
    if 'column' in data:
        document['column'] = data['column']
    document["data"] = [{
        'title': 'Safe to merge?',
        'type': 'BOOLEAN',
        'value': False
    }]
    return document


# with open(sys.stdin, "r") as messages:

if True:
    messages = sys.stdin
    linter = messages.readline().strip()
    # print("file_name {}".format(linter))
    file_type = messages.readline().strip()
    file_name = messages.readline().strip()
    count = int(messages.readline().strip())
    # print("file_name {}".format(file_name))
    # load the correct module

    good = count > 0
    if count > 0:
        failed = "FAILED"
    else:
        failed = "PENDING"
    report(count, {
        'result': failed,
        'safe': good,
        'details': 'na',
        'message': 'na'
    })

    new_total = -1
    try:
        mod = importlib.import_module("{}.{}".format('bb', linter))

        parser = mod.Parser(linter, file_type, file_name)
        result = parser.parse(messages)
        # pprint.pprint(result)
        new_total = count + len(result)

        if new_total > 0:
            failed = "FAILED"
            good = False
        else:
            failed = "PENDING"
            good = True
        report(new_total, {
            'result': failed,
            'safe': good,
            'details': 'na',
            'message': 'na'
        })
        # for problem in result:
        #     annotate_single(count, problem)
        #     count += 1
        annotate_batch(count, result)
    finally:
        print(new_total)
