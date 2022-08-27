# imports
import csv

# Hub for communication between the user and the algo #
from view.textView import textView

class userComms:

    controlCenter = None
    view = None
    userInput = dict()

    def __init__(self):
        self.log = open('model/log', 'w')
        self.writer = csv.writer(self.log)
        self.view = textView()

    ## Obtain User Input Necessary for Instantiation of the Algorithm and its Fields ##
    def collectUserInput(self):

        self.transmitMessage("Obtaining User Inputs...")

        ## Paper Trading or Realtime Trading ##
        while True:
            try:
                self.view.renderMessage("Type paper for Paper Trading or real for non-simulated trading:")
                pOrR = input()
                if pOrR == "paper" or pOrR == "real":
                    if pOrR == "paper":
                        self.userInput["ibkrCode"] = 7497
                    else:
                        self.userInput["ibkrCode"] = 7496
                else:
                    raise Exception
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

        ## Inform user of strategy choices ##
        self.view.renderMessage("\n---------- Strategy Library: ----------\n")
        i = 0
        for s in self.controlCenter.strategies:
            i += 1
            self.view.renderMessage(str(i) + ") " + s.description)

        # User Input: Strategy To Trade
        while True:
            try:
                strategyNumber = int(input("Enter the number of the strategy to be traded: "))
                self.userInput["strategy"] = self.controlCenter.strategies[strategyNumber - 1]
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

        # User Input: Balance to Trade
        while True:
            try:
                self.userInput["positionSize"] = int(input("Enter the desired position size: "))
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

    def transmitMessage(self, msg):
        self.view.renderMessage(msg)
        self.writer.writerow(msg)

        ## Connect to the Control Center for communication with other pieces of the algo ##

    def connectControlCenter(self, cc):
        self.controlCenter = cc