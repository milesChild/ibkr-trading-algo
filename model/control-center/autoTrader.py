# imports:
import time


# Delegates trade qualifications to the strategies. If a trade is qualified, then it requests order information
# from that strategy and transmits it to the ibkr comms. object.

class autoTrader:

    def __init__(self, userComms, ibkrComms):
        self.userComms = userComms
        self.ibkrComms = ibkrComms
        self.strategies = dict() # Strategy -> Contracts
        self.positionSize = 0

    # Strategies: dict(Strategy -> Contracts to be traded for that strategy)
    def setStrategies(self, strategies):
        self.strategies = strategies

    def setPositionSize(self, positionSize):
        self.positionSize = positionSize

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