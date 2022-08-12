## Class to Handle Storage of Market Data Streams from IBKR to be Used By Strategies ##
import multiprocessing
import pytz
import math
from datetime import datetime
import time

reqId = 1

class dataCenter:
    dataStreams = dict()
    ib = None
    global reqId
    timeframe = 1  # Requests only the highest granularity of data
    processIdCache = dict()
    initialbartime = datetime.now().astimezone(pytz.timezone("America/New_York"))
    delayFactor = .5

    ## To construct a dataCenter with an interactive brokers connection object
    def __init__(self, ib, contracts):
        self.ib = ib
        self.ib.connectDataCenter(self)

        for c in contracts:
            self.dataStreams[c] = []
            self.processIdCache[c] = -1

    def streamData(self):

        ## Collect Historical Data to Catch Up And Begin Trading ##
        print("Streaming Data")
        print(len(self.dataStreams))
        if __name__ != "__main__":
            num_processes = len(self.dataStreams)
            with multiprocessing.Pool(processes=num_processes) as pool:
                for c in self.dataStreams:
                    pool.map(self.collectHistoricalData(c), [])
            pool.close()

    def collectHistoricalData(self, contract):
        self.delayFactor += .5
        time.sleep(self.delayFactor)

        global reqId
        mintext = " min"
        if (int(self.timeframe) > 1):
            mintext = " mins"

        self.ib.reqHistoricalData(reqId, contract, "", "2 D", str(self.timeframe) + mintext, "TRADES", 1, 1,
                                  True,
                                  [])

        # Update the reqId for contract identification in processesIdCache
        self.processIdCache[contract] = reqId
        reqId += 1
        print("Initialized Data Stream for: " + str(contract.symbol) + "\n")

    def updateData(self, reqId, bar, realtime):

        key_list = list(self.processIdCache.keys())
        val_list = list(self.processIdCache.values())
        contractPosition = val_list.index(reqId)
        contractInHand = key_list[contractPosition]

        # Historical Data to catch up
        if (realtime == False):
            self.dataStreams[contractInHand].append(bar)
        else:
            bartime = datetime.strptime(bar.date, "%Y%m%d %H:%M:%S").astimezone(pytz.timezone("America/New_York"))
            minutes_diff = (bartime - self.initialbartime).total_seconds() / 60.0

            # On Bar Close
            if (minutes_diff > 0 and math.floor(minutes_diff) % self.timeframe == 0):
                self.dataStreams[contractInHand].append(bar)
                print("Added new bar for: " + str(contractInHand.symbol))
                time.sleep(1)
                print(self.dataStreams[contractInHand])