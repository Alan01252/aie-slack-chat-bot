import requests
import os

import time


class CheckedInByWeekGetter(object):
    def __init__(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.locations = ['utrecht', 'working from home', 'holborn', 'aston', 'woking']
        self.cache = {}

    def get_user_data(self, username):

        try:
            user_response = self.cache[username]
        except KeyError:
            print "Looking up user"
            url = os.environ['USER_ENDPOINT'] + username + '/details'
            print url
            user_response = requests.get(url)
            print user_response.status_code
            self.cache[username] = user_response.json()
            user_response = self.cache[username]

        return user_response

    def get_email(self, username):
        user_data = self.get_user_data(username)
        return user_data["emailAddress"]

    def get_name(self, username):
        user_data = self.get_user_data(username)
        return user_data['forename'] + ' ' + user_data['surname']  # Lazyyy

    def get_checked_in(self):
        response = requests.get(os.environ['ANALYTICS_ENDPOINT'])
        data = response.json()

        checked_in = {}

        for user in data:
            username = user["username"]
            checked_in[username] = {}
            for day in self.days:
                checked_in[username][day] = ""
                for location in self.locations:
                    if any(emotion > 0 for emotion in user[day][location]['in'].values()):
                        checked_in[username][day] = location

        response = "Name, Email, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday \n"
        for user in checked_in:
            #Without this get weird 404 occasionally WTF can't be bothered to figure out why
            time.sleep(0.1)
            user_email = self.get_email(user)
            user_name = self.get_name(user)

            response += user_name + "," + user_email + "," + checked_in[user]['Monday'] + "," \
                  + checked_in[user]['Tuesday'] + "," \
                  + checked_in[user]['Wednesday'] + "," \
                  + checked_in[user]['Thursday'] + "," \
                  + checked_in[user]['Friday'] + "," \
                  + checked_in[user]['Saturday'] + "," \
                  + checked_in[user]['Sunday'] + " \n"

        return response


