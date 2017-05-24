import logging
import json
import os

from urlparse import parse_qs
from urllib2 import Request, urlopen, URLError, HTTPError

from slackbot.CheckedInTodayGetter import CheckedInTodayGetter
from slackbot.HelpGetter import HelpGetter
from slackbot.RegisterGetter import RegisterGetter
from slackbot.Registerer import Registerer

print('Loading AIE slackbot')

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def getHelp(command_text=None):
    helpGetter = HelpGetter()
    return helpGetter.get_help_message()


def getRegistered(command_text=None):
    registerGetter = RegisterGetter()
    return registerGetter.getRegistered()

def get_checked_in(location):
    checked_in = CheckedInTodayGetter()
    return checked_in.get_checked_in(location)


def register(command_text=None):
    registerer = Registerer()
    return registerer.register(command_text);


def sendResponseMessage(message, url):
    slack_message = {
        'text': message
    }

    req = Request(url, json.dumps(slack_message))

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
    args = ""

    if params.has_key("text"):
        command_text = params['text'][0].split()[0]
        args = params['text'][0]
    else:
        command_text = "help"

    command = {
        'help': getHelp,
        'get_registered': getRegistered,
        'register': register
    }

    if command_text == "register":
        sendResponseMessage("Trying to send check in/out response for you now", params["response_url"][0])

    message = command[command_text](args)

    sendResponseMessage(message, params["response_url"][0])

    return True
