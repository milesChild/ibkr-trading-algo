"""
Class to handle mediation of entries, exits, and RM of positions.
"""
class newTrader:
    riskManager = None # object that handles rm
    strategies = None

    def __init__(self):
        self.initializeStrategies()

    def runLoop(self):
        # first, check the time and either update necessary data for positions or close them
        self.checkTime()
        # second, make sure we are at healthy risk levels before continuing to trade
        self.manageRisk()
        # third, search for positions to enter
        self.enterTrades()
        # fourth, manage current positions
        self.managePositions()

    def initlaizeStrategies(self):
        return

    """
    If the time is before 9:29 then stop all systems and wait for 9:29
    If the time is 3:59 then begin closing positions and quit looking for new positions
    Otherwise do nothing
    """
    def checkTime(self):
        if