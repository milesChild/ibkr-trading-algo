from ibapi.order import Order

from IStrategy import IStrategy

# Strategy For Testing Only #
class higherHigh(IStrategy):

    def __init__(self):
        self.description = "Entry: Higher High (USED FOR TESTING PURPOSES)"
        self.timeframe = 1
        global orderId

    def determineEntry(self, bars, currBar):

        # Entry - If we have a higher high then Buy
        
        lastHigh = bars[len(bars) - 2].high
        recentHigh = bars[len(bars) - 1].high

        print("Last High:" + str(lastHigh))
        print("Most Recent High:" + str(recentHigh))

        # Check Criteria
        if currBar.high > lastHigh:
            return True

    def bracketOrder(self, parentOrderId, quantity, contract, last):
        profitTarget = last * 1.01
        stopLoss = last * .995

        # Initial Entry
        # Create Parent Order / Initial Entry
        parent = Order()
        parent.orderId = parentOrderId
        parent.orderType = "MKT"
        parent.action = "BUY"
        parent.totalQuantity = quantity
        parent.transmit = False
        # Profit Target
        profitTargetOrder = Order()
        profitTargetOrder.orderId = parent.orderId + 1
        profitTargetOrder.orderType = "LMT"
        profitTargetOrder.action = "SELL"
        profitTargetOrder.totalQuantity = quantity
        profitTargetOrder.lmtPrice = round(profitTarget, 2)
        profitTargetOrder.parentId = parentOrderId
        profitTargetOrder.transmit = False
        # Stop Loss
        stopLossOrder = Order()
        stopLossOrder.orderId = parent.orderId + 2
        stopLossOrder.orderType = "STP"
        stopLossOrder.action = "SELL"
        stopLossOrder.totalQuantity = quantity
        stopLossOrder.parentId = parentOrderId
        stopLossOrder.auxPrice = round(stopLoss, 2)
        stopLossOrder.transmit = True

        bracketOrders = [parent, profitTargetOrder, stopLossOrder]
        return bracketOrders
