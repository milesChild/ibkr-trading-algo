# imports
import userComms
import autoTrader
import ibkrComms

## USER RUNS PROGRAM HERE ##
from model.strategies.bullbreakout import bullbreakout
from model.strategies.higherHigh import higherHigh
from model.strategies.nineEmaCrossoverHigherHighAndLow import nineEmaCrossoverHigherHighAndLow


class controlCenter:

    strategies = []

    def __init__(self):
        self.userComms = userComms()
        self.autoTrader = autoTrader()
        self.ibkrComms = ibkrComms()

        self.userComms.connectControlCenter(self)
        self.autoTrader.connectControlCenter(self)
        self.ibkrComms.connectControlCenter(self)

        self.run()

    # Internal Clock
    def run(self):
        self.userComms.collectUserInput()

    ## CONFIGURABLE - Enter the strategies the user can choose from here ##
    ## TODO: Make better
    def initializeStrategies(self):
        ## Append each of the desired strategies to trade to the strategy book ##
        self.strategies.append(nineEmaCrossoverHigherHighAndLow())
        self.strategies.append(higherHigh())
        self.strategies.append(bullbreakout())