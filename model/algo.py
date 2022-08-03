## Imports ##
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract
import pytz
import math
from datetime import datetime, timedelta
import threading
from model.bar import Bar
from model.strategies.higherHigh import higherHigh
from model.strategies.nineEmaCrossoverHigherHighAndLow import nineEmaCrossoverHigherHighAndLow
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from view.textView import textView

orderId = 1


## Algorithm to Handle Trade Execution ##

class Algo:
    availableFunds = 0
    balance = 1000
    ib = None  # Interactive Brokers connection
    currentBar = Bar()  # Current candle
    reqId = 1  # Current request id for pulling data from IBKR
    global orderId  # Current order id for placing trades thru IBKR
    initialbartime = datetime.now().astimezone(pytz.timezone("America/New_York"))
    contract = None  # Current contract in-hand
    strategies = []  # Book of strategies that can be traded (CONFIGURABLE)
    positionSize = 0
    ibkrCode = 0
    view = textView()
    bars = []

    def __init__(self):
        self.initializeStrategies()
        self.obtainUserInput()
        self.connectToIBKR()

        ## Start the trading process ##
        self.view.renderMessageAndPause("System Starting...")

        ## Update Information ##
        self.positionSize = round(int(self.balance) / 2)  # 2 represents the total number of trades that will be placed
        self.initContracts()
        self.currentBar = Bar()
        self.timeframe = self.strategy.timeframe
        self.queryTime = (datetime.now().astimezone(pytz.timezone("America/New_York")) - timedelta(days=1)).replace(
            hour=16,
            minute=0,
            second=0,
            microsecond=0).strftime(
            "%Y%m%d %H:%M:%S")
        self.ib.reqIds(-1)

        ## Collect Historical Data to Catch Up And Begin Trading ##
        self.collectHistoricalData()

    ## CONFIGURABLE - Enter the contracts for the Algo to cycle here ##
    ## TODO: Make compatable for multiple contracts
    def initContracts(self):
        SPY = Contract()
        SPY.symbol = "SPY"
        SPY.secType = "STK"
        SPY.exchange = "SMART"
        SPY.currency = "USD"

        AAPL = Contract()
        AAPL.symbol = "AAPL"
        AAPL.secType = "STK"
        AAPL.exchange = "SMART"
        AAPL.currency = "USD"

        QQQ = Contract()
        QQQ.symbol = "QQQ"
        QQQ.secType = "STK"
        QQQ.exchange = "SMART"
        QQQ.currency = "USD"

        self.contract = SPY

    ## CONFIGURABLE - Enter the strategies the user can choose from here ##
    def initializeStrategies(self):

        ## Append each of the desired strategies to trade to the strategy book ##
        self.strategies.append(nineEmaCrossoverHigherHighAndLow())
        self.strategies.append(higherHigh())

    ## Connect to IBKR TWS upon initialization ##
    def connectToIBKR(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", self.ibkrCode, 1)  # 7497 = paper, 7496 = real trading
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()

    ## Obtain User Input Necessary for Instantiation of the Algorithm and its Fields ##
    def obtainUserInput(self):

        ## Paper Trading or Realtime Trading ##
        while True:
            try:
                self.view.renderMessage("\nType paper for Paper Trading or real for non-simulated trading:\n")
                pOrR = input()
                if pOrR == "paper" or pOrR == "real":
                    if pOrR == "paper":
                        self.ibkrCode = 7497
                    else:
                        self.ibkrCode = 7496
                else:
                    raise Exception
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

        ## Inform user of strategy choices ##
        self.view.renderMessage("\n---------- Strategy Library: ----------\n")
        i = 0
        for s in self.strategies:
            i += 1
            self.view.renderMessage(str(i) + ") " + s.description + "\n")

        # User Input: Strategy To Trade
        while True:
            try:
                strategyNumber = int(input("Enter the number of the strategy to be traded: \n"))
                self.strategy = self.strategies[strategyNumber - 1]
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

        # User Input: Balance to Trade
        while True:
            try:
                self.positionSize = int(input("Enter the desired position size: \n"))
                break
            except Exception:
                self.view.renderMessage("Invalid Entry. Try Again...")

    # Initializes the account balance for trading #
    ## TODO: This will not work unless we periodically check the user's balance because the user might place trades while the algo is running, further depleting the balance
    def obtainAccountInfo(self):
        self.availableFunds = self.ib.reqAccountSummary(self.reqId, "All", AccountSummaryTags.AvailableFunds)
        self.reqId += 1

    def collectHistoricalData(self):

        ## Request Market Data ##
        self.view.renderMessage("\n" + "Collecting Historical Data..." + "\n")

        mintext = " min"
        if (int(self.timeframe) > 1):
            mintext = " mins"

        self.ib.reqHistoricalData(self.reqId, self.contract, "", "2 D", str(self.timeframe) + mintext, "TRADES", 1, 1,
                                  True,
                                  [])
        self.reqId += 1

    # Listen to socket in seperate thread
    def run_loop(self):
        self.ib.run()

    # Pass realtime bar data back to our bot object
    def on_bar_update(self, reqId, bar, realtime):

        global orderId

        # Historical Data to catch up
        if (realtime == False):
            self.bars.append(bar)
        else:
            bartime = datetime.strptime(bar.date, "%Y%m%d %H:%M:%S").astimezone(pytz.timezone("America/New_York"))
            minutes_diff = (bartime - self.initialbartime).total_seconds() / 60.0

            # On Bar Close
            if (minutes_diff > 0 and math.floor(minutes_diff) % self.timeframe == 0):
                self.initialbartime = bartime

                self.view.renderMessage("New bar for symbol: " + self.contract.symbol + "\n")
                self.view.renderMessage("Checking strategy criteria for symbol: " + self.contract.symbol + "\n")

                if self.strategy.determineEntry(self.bars, bar):
                    self.view.renderMessage("Initiating position in symbol: " + self.contract.symbol + "\n")
                    self.placeOrder(bar.close)

                # Bar closed append
                self.bars.append(bar)

    def placeOrder(self, close):
        global orderId

        self.view.renderMessage("Strategy triggered...\n")
        self.view.renderMessage("Placing order...\n")
        qty = self.calculateQuantity(close)

        # Do not place order if it will cause a negative balance
        if qty * close > self.balance:
            self.view.renderMessage("Insufficient funds for trade...")
            return

        bracket = self.strategy.bracketOrder(orderId, qty,
                                             self.contract, close)
        for o in bracket:
            o.ocaGroup = "OCA_" + str(orderId)
            self.ib.placeOrder(o.orderId, self.contract, o)
        orderId += 3

        # Decrement balance based on the value of the trade placed
        self.balance -= qty * close

    # Not finished: Need more elaborate quantity calculation
    def calculateQuantity(self, close):
        return round(self.positionSize / close)


## Connection to Interactive Brokers ##

class IBApi(EWrapper, EClient):
    view = textView()

    def __init__(self):
        EClient.__init__(self, self)

        ## Callbacks ##

    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            self.view.renderMessage(e)

    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
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
            bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
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


bot = Algo()
