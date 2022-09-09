# imports

# Class for communication to/from interactive brokers
import threading
import time
from oldmodel.ibkrConnection import IBApi

class ibkrComms:
    controlCenter = None

    def __init__(self):
        self.connectToIBKR()

    ## Connect to IBKR TWS upon initialization ##
    def connectToIBKR(self):
        self.ib = IBApi()
        self.ib.connectAlgo(self)
        self.ib.connect("127.0.0.1", self.ibkrCode, 1)  # 7497 = paper, 7496 = real trading
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

    ## Connect to the Control Center for communication with other pieces of the algo ##
    def connectControlCenter(self, cc):
        self.controlCenter = cc

    # Takes a non-empty list of orders and transmits them to Interactive Brokers to be executed.
    # Notifies the user every time an order is placed.
    # orders: list[dict(symbol -> order)]
    def transmitOrder(self, orders):
        global orderId

        for pair in orders:

            contract = pair.key
            o = pair.value

            # If the current order is a bracket order, then send all suborders
            if isinstance(o, list):
                for bo in o:
                    bo.ocaGroup = "OCA_" + str(orderId)
                    self.ib.placeOrder(bo.orderId, contract, bo)
                    orderId += 3
                    ## Placing Order: BUY/SELL 100 SPY
                    self.userComms.transmitMessage("Placing Order: " + str(bo.action) + " " + bo.totalQuantity
                                                   + " " + str(contract.symbol))
            # If the current order is not a bracket order, just send the order
            else:
                o.ocaGroup = "OCA_" + str(orderId)
                self.ib.placeOrder(o.orderId, contract, o)
                orderId += 1
                self.userComms.transmitMessage("Placing Order: " + str(o.action) + " " + o.totalQuantity
                                               + " " + str(contract.symbol))