# imports
import csv

# Hub for communication between the user and the algo #
class userComms:

    def __init__(self):
        self.log = open('model/log', 'w')
        self.writer = csv.writer(self.log)

    ## TODO
    def collectUserInput(self):
        return

    def transmitMessage(self, msg):
        self.view.renderMessage(msg)
        self.writer.writerow(msg)