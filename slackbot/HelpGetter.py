class HelpGetter(object):
    def __init__(self):
        print "in help getter"

    def is_not_used(self):
        pass

    def get_help_message(self):

        self.is_not_used();

        return "Welcome to the AIE Bot " \
               "\n\n Current commands: \n\n " \
               "help : Returns this message \n\n " \
               "get_registered : Returns a link to get a spreadsheet of users \n\n" \
               "register : ChecksIn/Out of a location \n\n" \
               "        Usage: /aie register [UserName] [Location] e.g /aie register AlanHollis Working From Home"
