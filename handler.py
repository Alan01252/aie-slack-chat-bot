import logging
import json
import os

from urlparse import parse_qs
from urllib2 import Request, urlopen, URLError, HTTPError

from slackbot.HelpGetter import HelpGetter
from slackbot.RegisterGetter import RegisterGetter

print('Loading AIE slackbot')

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def getHelp():
    helpGetter = HelpGetter()
    return helpGetter.getHelpMessage()


def getRegistered():
    registerGetter = RegisterGetter()
    return registerGetter.getRegistered()


def sendMessage(message):
    hook_url = os.environ["SLACK_HOOK_URL"]

    slack_message = {
        'text': message
    }

    req = Request(hook_url, json.dumps(slack_message))

    try:
        response = urlopen(req)
        response.read()
    except HTTPError as e:
        log.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        log.error("Server connection failed: %s", e.reason)

    response = {
        "statusCode": 200,
        "body": message
    }

    return response


def start(event, context):
    assert context
    log.debug(event)

    req_body = event['body']
    params = parse_qs(req_body)

    if params.has_key("text"):
        command_text = params['text'][0]
    else:
        command_text = "help"

    message = {
        'help': getHelp(),
        'get_registered': getRegistered()
    }.get(command_text, "Command not found" + command_text + "\n\n" + getHelp())

    return sendMessage(message)
