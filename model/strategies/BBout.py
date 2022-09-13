
class BBout:
    """
    New Strategy Example

    Strategy Explanation:

    BUY when the price crosses the price level that corresponds to the avg. price during the highest volume 5min interval
    during the previous day.

    SELL when the P/L on the order has reached .25% PT or (.15%) SL.

    Assume backtesting returned a W/L ratio > 50%.

    Entries and exits are not scaled. All trading occurs intraday (de-risk from this strategy before the bell).
    """
    interday = False  # Only traded within the same day
    scaledEntry = False  # Total entry occurs in one singular order
    scaledExit = False  # Total entry occurs in one singular order
    historicalData = dict()  # Storage area for necessary historical data
    contracts = []

    def __init__(self):
        self.historicalData = {"TriggerPrice": dict(), "LastTick": dict()}
        self.collectHistoricalData()

    def collectHistoricalData(self):
        """
        Collects the necessary historical data from the polygon api by populating the TriggerPrice and LastTick fields. 
        """
        return

    def determineEntry(self, tickData, contract):
        """
        Determines whether an entry into a contract should be made given:
       - The strategy parameters for entry
       - The current price on this 1sec tick
       - The previous tick 
       - The trigger price for this particular contract

        Note: I do not know how data will be passed by polygon, so I am assuming that the "tickData"
        will not just be a simple last price.
        """
        tick = tickData.price
        # if bull breakout then enter
        if tick >= self.historicalData["TriggerPrice"][contract] and \
                self.historicalData["LastTick"][contract] < self.historicalData["TriggerPrice"][contract]:
            o = self.generateOrder("BUY", tickData, contract)
        else:
            o = False
        # update the "last tick" in historical data
        self.historicalData["LastTick"][contract] = tick
        return o

    def determineExit(self, tickData, order):
        # stop-loss / profit-target handled in one line
        tick = tickData.price
        if tick <= order.fillPrice * .9985 or tick >= order.fillPrice * 1.0025:
            return self.generateOrder("SELL", tickData, order.contract)
        # in the trader, make sure the order status is updated to closed after the exit is filled


"""
What is missing?

  - Scaled entries & exits implementation
  - Order logging/storage of necessary information
  - Error handling
  - Specifics on how collectHistoricalData will be implemented/refreshed according to the strategy's requirements
  
"""
