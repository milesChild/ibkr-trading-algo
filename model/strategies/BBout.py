from model.broker.order import Side, Order


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

    def enter_trades(self, tickData):
        trades = []
        for contract in self.contracts:
            trades.append(self.__determine_entry(tickData[contract.symbol]["p"], contract))  # gets the "price" section of the respective contract entry in the JSON

        return trades

    # Accepts a list of positions and determines if additional entries (for scaled entry positions) or exits should be
    # made
    def manage_positions(self, tickData, positions):
        trades = []
        for position in positions:
            # No scaled entries in this one, so all we have to do is check for exits
            trades.append(self.__determine_exit(tickData[position.contract.symbol]["p"], position))

    def __determine_entry(self, last, contract):
        """
        Determines whether an entry into a contract should be made given:
       - The strategy parameters for entry
       - The current price on this 1sec tick
       - The previous tick 
       - The trigger price for this particular contract

        Note: I do not know how data will be passed by polygon, so I am assuming that the "tickData"
        will not just be a simple last price.
        """
        # if bull breakout then enter
        if last >= self.historicalData["TriggerPrice"][contract] and \
                self.historicalData["LastTick"][contract] < self.historicalData["TriggerPrice"][contract]:
            self.historicalData["LastTick"][contract] = last
            return self.__generate_order(Side.BUY, last, contract)
        # update the "last tick" in historical data
        self.historicalData["LastTick"][contract] = last

    # Takes a position and determines whether an exit should be made
    # In this particular case, there are no partial exits so its all or nothing
    def __determine_exit(self, last, position):
        # stop-loss / profit-target handled in one line
        avg = position.__calc_avg()
        if last <= avg * .9985 or last >= avg * 1.0025:
            return self.__generate_order(Side.SELL, position.contract)
        # in the trader, make sure the order status is updated to closed after the exit is filled

    def __generate_order(self, type, last, contract):
        qty = self.__calculate_qty(contract, last)
        return Order(type, qty, contract)

    def __generate_order(self, type, position):
        qty = 0
        return Order(type, qty, position)

    def __calculate_qty(self, contract, last):
        # TODO: Figure out optimal position sizing based on the strategy
        return 0

"""
What is missing?

  - Scaled entries & exits implementation
  - Order logging/storage of necessary information
  - Error handling
  - Specifics on how collectHistoricalData will be implemented/refreshed according to the strategy's requirements
  
"""
