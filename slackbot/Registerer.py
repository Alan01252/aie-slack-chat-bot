import base64
import os

from PIL import Image
import cStringIO

import requests


class Registerer(object):
    def getImageData(self, args):

        print "Getting image for user " + args[1]

        response = requests.get(os.environ['USER_ENDPOINT'] + args[1] + "/details",
                                headers={'Origin': os.environ["AUTH_HEADER"]})

        json = response.json()
        image = json["profileImage"]

        img_str = base64.b64encode(requests.get(image).content)

        return "data:image/jpeg;base64," + img_str

    def performRegistration(self, args, imageData):

        data = {
            'Image': imageData,
            'Location': " ".join(args[2::]),
            'quick': 1,
        }

        print "Sending request to check in url"

        response = requests.post(os.environ["CHECK_IN_URL"], data)

        if response.status_code == 200:
            return True
        else:
            return False

    def register(self, command_text):
        args = command_text.split()

        print args

        imageData = self.getImageData(args)
        if self.performRegistration(args, imageData) == True:
            print "Check-in Success"
            return "CheckIn/Out Successfull"
        else:
            print "Check-in Failed"
            return "CheckIn/Out Failed"
