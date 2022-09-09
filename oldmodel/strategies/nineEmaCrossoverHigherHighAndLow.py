from ibapi.contract import Contract
from ibapi.order import Order

from oldmodel.strategies.IStrategy import IStrategy
import ta
import numpy as np
import pandas as pd

class nineEmaCrossoverHigherHighAndLow(IStrategy):

    def __init__(self):
        self.description = "Entry: Cross of 9ema, Higher High, Higher Low"
        self.timeframe = 1
        global orderId
        self.smaPeriod = 9

    def determineEntry(self, bars, currBar):

        # Entry - If we have a higher high, a higher low and we cross the 50 SMA Buy
        # 1.) SMA
        closes = []
        for bar in bars:
            closes.append(bar.close)
        close_array = pd.Series(np.asarray(closes))
        sma = ta.trend._sma(close_array, self.smaPeriod, True)
        print("SMA : " + str(sma[len(sma) - 1]))

        # 2.) Calculate Higher Highs and Lows
        lastBar = bars[len(bars) - 1]
        lastLow = lastBar.low
        lastHigh = lastBar.high
        lastClose = lastBar.close

        # Check Criteria
        if (currBar.close > lastHigh
                and currBar.low > lastLow
                and currBar.close > sma[len(sma) - 1]
                and lastClose < sma[len(sma) - 2]):
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