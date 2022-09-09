# imports:
import time

# Delegates trade qualifications to the strategies. If a trade is qualified, then it requests order information
# from that strategy and transmits it to the ibkr comms. object.

class autoTrader:
    controlCenter = None
    positionSize = 0
    strategies = dict()

    def __init__(self):
        self.positionSize = 0
        self.strategies = dict() # Strategy -> Contract[]

    ## Connect to the Control Center for communication with other pieces of the algo ##
    def connectControlCenter(self, cc):
        self.controlCenter = cc

    def reqUserInputs(self):
        ps = self.controlCenter.userComms.userInput["positionSize"]
        s = self.controlCenter.userComms.userInput["strategies"]

        self.positionSize = ps
        self.strategies = s

    def searchForTrades(self):

        tradesQueue = []

        for s in list(self.strategies.keys()):
            if s.determineEntry():
                tradesQueue.append(s)

        if tradesQueue.count() > 0:
            self.collectOrders(tradesQueue)

    def collectOrders(self, tradesQueue):
        orders = []

        for s in tradesQueue:
            orders.append(s.entryOrder)

        self.transmitOrders(orders)

    def transmitOrders(self, orders):
        self.ibkrComms.sendOrders(orders)
        self.userComms.transmitMessage("Transmitting Orders to Interactive Brokers...")