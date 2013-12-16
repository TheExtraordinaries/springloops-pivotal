#!/usr/bin/env python

""" pusher.py - This is where the magic happens -- takes in springloops input, pushes the message to pivotal"""

import requests
import re
import json

TOKEN = 'xxxxx'

def pushToPivotal(springloopsData):
    """This pushes the commit message from springloops to pivotal"""

    if 'payload' in springloopsData:
        payload = springloopsData['payload']

        # We must take out the print formatting before loading the json
        unencodedData = json.loads(payload.replace('\\n',' '))

        if 'commits' in unencodedData and 'commit' in unencodedData['commits']:
            springloopsData = unencodedData['commits']['commit']
        else:
            return False
    else:
        return False

    if "commitMessage" not in springloopsData:
        return False
    else:
        springloopsData['commitMessage'] = processCommitMessage(springloopsData['commitMessage'])
        if not springloopsData['commitMessage']:
            return False

    fields = ['committerName', 'commitMessage', 'revision', 'commitURL']
    for field in fields:
        if field not in springloopsData:
            springloopsData[field] = ""

    data = {
        "source_commit":
        {
            "author": springloopsData['committerName'],
            "message": springloopsData['commitMessage'],
            "commit_id": springloopsData['revision'],
            "url": springloopsData['commitURL']
        }
    }

    ret = pivotalAPI("/source_commits",data)
    if ret:
        return True
    else:
        return False


def processCommitMessage(commitMessage):
    """This will process the a commit message with story links into a nicely formatted links for pivotal consumption

    >>>print processCommitMessage("Fixing [finished] https://www.pivotaltracker.com/story/show/123 https://www.pivotaltracker.com/story/show/321")
    Fixing [finished #123 #321]
    """
    replaceThese = []
    storyIds = []
    existingTags = []

    # Step 1 - find all of the links
    storyLinks = re.findall(r'https://www.pivotaltracker.com/story/show/[0-9]+', commitMessage)
    if storyLinks:
        for storyLink in storyLinks:
            replaceThese.append(storyLink)
            storyIds.append(storyLink[42:])

     # Step 2 - find existing tags so we don't overwrite those
    existingTagString = re.findall(r'\[.+\]', commitMessage)
    for tags in existingTagString:
        replaceThese.append(tags)
        existingTags.append(tags[1:-1])

    # If there are no links or existing tags, there's no point to this
    if not storyLinks and not existingTagString:
        return False

    # Step 3 - remove all of the links from the commit message
    for sbstr in replaceThese:
        commitMessage = commitMessage.replace(sbstr, '')

    # Step 4 - Build the tag string
    tagString = ""
    usePrecedingSpace = False

    for existingTag in existingTags:
        if usePrecedingSpace:
            tagString += " "
        else:
            usePrecedingSpace = True

        tagString += existingTag

    for storyId in storyIds:
        if usePrecedingSpace:
            tagString += " "
        else:
            usePrecedingSpace = True

        tagString += "#" + storyId

    commitMessage += " [" + tagString + "]"

    # Step 5 - Format for HTML
    commitMessage = escape(commitMessage)

    return commitMessage


def escape(s):
    """Taken from python's html library in 3.x escapes the html for python

    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    Also translates the double quote and single quote chars, as well as
    performs a simple nl2br operation.
    """
    escapeMap = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;',
                    ord('"'): '&quot;', ord('\''): '&#x27;', ord('\n'): '<br> '}
    return s.translate(escapeMap)


def pivotalAPI(path, payload, method="POST"):
    """Simple wrapper for the pivotal API"""

    header = {'X-TrackerToken': TOKEN}

    requestUrl = 'https://www.pivotaltracker.com/services/v5/' + path

    if method == "POST":
        header['Content-Type'] = 'application/json'
        payload = json.dumps(payload)
        response = requests.post(requestUrl, data=payload, headers=header)
    else:
        response = requests.get(requestUrl, data=payload, headers=header)

    return response.json()


if __name__ == '__main__':
    print pushToPivotal({'committerName': 'Patrick Grennan', 'commitMessage': "New test [finished] https://www.pivotaltracker.com/story/show/62416424"})
