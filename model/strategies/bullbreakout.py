from ibapi.order import Order

def determineEntry(bars,currBar):
    #Checks if most recent bar is higher than previous bar
    if currBar > bars[len(bars) - 1].high:
        #sorts into most recent 4 candles
        checkList = bars[(len(bars) - 5):(len(bars) - 1)]
        #loops to make sure every succeding candle is lower than the last
        while checkList != []:
            #check highs
            index1 = bars.index(checkList[0])
            index2 = bars.index(checkList[1])
            high1 = index1.high
            high2 = index2.high
            if high1 < high2: return False
            checkList = checkList[1::]
        #enter if most recent candle is first green after 4 red candles
        return True
    return False

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
