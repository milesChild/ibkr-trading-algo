# imports

# Class for communication to/from interactive brokers
import threading
import time

from model.ibkrConnection import IBApi


class ibkrComms:

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

    def transmitOrder(self, order):
        global orderId

        ## if bracket, then
        for o in bracket:
            o.ocaGroup = "OCA_" + str(orderId)
            self.ib.placeOrder(o.orderId, contract, o)
        orderId += 3

        ## else
        self.ib.placeOrder(order.orderId, order.contract, order)
        orderId += 1