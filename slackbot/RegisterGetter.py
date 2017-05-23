import json
import os

import requests

class RegisterGetter(object):
    def __init__(self):
        print "in register getter"

    def getRegistered(self):

        response = requests.get(os.environ['REGISTER_ENDPOINT'],
                     headers={'Origin': os.environ["AUTH_HEADER"]})

        data = response.json()
        for row in data["rows"]:
            print row["fields"]["meta_username"]

        return json.dumps(data)

#registerGetter = RegisterGetter()
#registerGetter.getRegistered();