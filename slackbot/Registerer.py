import base64
import os
import requests


class Registerer(object):

    def is_not_used(self):
        pass

    def check_currently_available(self, args):

        self.is_not_used()

        print "Getting availability for user " + args[1]

        response = requests.get(
            os.environ['ANALYTICS_SERVICE'] + "/location/" + " ".join(args[2::]) + "/availability/now",
            headers={'Origin': os.environ["AUTH_HEADER"]})

        json = response.json()

        try:
            for row in json["users"]:
                if row["username"] == args[1]:
                    return True
        except KeyError:
            return False

        return False

    def get_image_data(self, args):

        self.is_not_used()

        print "Getting image for user " + args[1]

        response = requests.get(os.environ['USER_ENDPOINT'] + args[1] + "/details",
                                headers={'Origin': os.environ["AUTH_HEADER"]})

        json = response.json()
        image = json["profileImage"]

        img_str = base64.b64encode(requests.get(image).content)

        return "data:image/jpeg;base64," + img_str

    def perform_registration(self, args, imageData):

        self.is_not_used()

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

        imageData = self.get_image_data(args)

        checkedIn = self.check_currently_available(args)

        message = "Check-In"
        if checkedIn:
            message = "Check-Out"

        if self.perform_registration(args, imageData) == True:
            return message + " Success"
        else:
            return message + " Failed"
