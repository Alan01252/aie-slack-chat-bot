import calendar
import datetime
import requests
import os


class CheckedInTodayGetter(object):
    def get_user_data(self, username):
        url = os.environ['USER_ENDPOINT'] + '{0}/details'.format(username)
        user_response = requests.get(url, headers={'Origin': os.environ['AUTH_HEADER']})
        return user_response.json()

    def get_email(self, username):
        user_data = self.get_user_data(username)
        return user_data["emailAddress"]

    def get_name(self, username):
        user_data = self.get_user_data(username)
        return user_data['forename'] + ' ' + user_data['surname']  # Lazyyy

    def get_checked_in(self, location):
        if location is None:
            location = 'holborn'
        response = requests.get(os.environ['ANALYTICS_ENDPOINT'],
                                headers={'Origin': os.environ['AUTH_HEADER']})

        data = response.json()

        today = calendar.day_name[datetime.datetime.today().weekday()]

        # Sorry for what you're about to read #startupcode
        # We'll go with getting just those who have checked in today
        # and returning a string of users/emails.
        # We'll filter on a location to make it easier.
        checked_in = {}
        # TODO: List comprehension instead of loop
        for user in data:
            username = user["username"]
            if any(emotion > 0 for emotion in user[today][location]['in'].values()):
                checked_in[self.get_name(username)] = self.get_email(username)

        return ', '.join('%s <%s>' % (key, val) for (key, val) in checked_in.items())


#checked_in_users = CheckedInTodayGetter()
#print checked_in_users.get_checked_in('holborn')

