
class scaledEntryBBout:
    interday = False  # Only traded within the same day
    scaledEntry = True  # Total entry occurs in one singular order
    scaledExit = False  # Total entry occurs in one singular order
    historicalData = dict()  # Storage area for necessary historical data
    contracts = []

    def __init__(self):
        self.historicalData = {"TriggerPrice": dict(), "LastTick": dict()}
        self.collectHistoricalData()

    """
    Collects the necessary historical data from the polygon api by populating the TriggerPrice and LastTick fields. 
    """
    def collectHistoricalData(self):
        return

    """
    Determines whether an entry into a contract should be made given:
       - The strategy parameters for entry
       - The current price on this 1sec tick
       - The previous tick 
       - The trigger price for this particular contract
    
    Note: Entries are scaled by 50%, 25%, 25% increments
    """
    def determineEntry(self, tickData, contract):
        tick = tickData.price
        # if bull breakout then enter
        if tick >= self.historicalData["TriggerPrice"][contract] > self.historicalData["LastTick"][contract]:
            o = self.generateScaledOrder("BUY", tick, contract)
        else:
            o = False
        # update the "last tick" in historical data
        self.historicalData["LastTick"][contract] = tick
        return o

    def determineExit(self, tickData, order):
        # stop-loss / profit-target handled in one line
        tick = tickData.price
        if tick <= order.fillPrice * .9985 or tick >= order.fillPrice * 1.0025:
            return self.generateOrder("SELL", tick, order.contract)
        # in the trader, make sure the order status is updated to closed after the exit is filled

    """
    Allows the trader to take a position in scaled entries...
    
    This particular strategy enters its first block @ 50% of total position size, then two more 25% increments.
    """
    def generateScaledOrder(self, executionType, price, contract, order):
        if order == None:
            # return an order @ 50% of the desired position size
            o = self.generateOrder("BUY", price, contract, .5)
        else:
            if order.filledAmount == .5 or .75:
                o = self.generateOrder("BUY", price, contract, .25)
        return o

    """
    Generates an order to be given to the trader to transmit to IBKR
    """
    def generateOrder(self):

