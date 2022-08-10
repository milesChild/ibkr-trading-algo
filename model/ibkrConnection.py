## Connection to Interactive Brokers ##
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from view.textView import textView

class IBApi(EWrapper, EClient):
    view = textView()
    algo = None
    dataCenter = None

    def __init__(self):
        EClient.__init__(self, self)

    def connectAlgo(self, algo):
        self.algo = algo

    def connectDataCenter(self, dataCenter):
        self.dataCenter = dataCenter

        ## Callbacks ##

    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            self.dataCenter.updateData(reqId, bar, False)
        except Exception as e:
            self.view.renderMessage(e)

    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        try:
            self.dataCenter.updateData(reqId, bar, True)
        except Exception as e:
            self.view.renderMessage(e)

    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        self.view.renderMessage(reqId)

    # Get next order id we can use
    def nextValidId(self, nextorderId):
        global orderId
        orderId = nextorderId

    # Listen for realtime bars
    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        try:
            self.dataCenter.updateData(reqId, time, open_, high, low, close, volume, wap, count)
        except Exception as e:
            self.view.renderMessage(e)

    def error(self, id, errorCode, errorMsg):
        self.view.renderMessage(errorCode)
        self.view.renderMessage(errorMsg)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        return value

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)