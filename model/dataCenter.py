## Class to Handle Storage of Market Data Streams from IBKR to be Used By Strategies ##
import multiprocessing
import pytz
import math
from datetime import datetime

class dataCenter:
    dataStreams = dict()
    ib = None
    timeframe = 1  # Requests only the highest granularity of data
    processIdCache = dict()

    ## To construct a dataCenter with an interactive brokers connection object
    def __init__(self, ib, contracts):
        self.ib = ib

        for c in contracts:
            self.dataStreams[c] = []
            self.processIdCache[c] = -1

    def streamData(self):

        ## Collect Historical Data to Catch Up And Begin Trading ##
        if __name__ == "__main__":
            num_processes = len(self.dataStreams)
            with multiprocessing.Pool(processes=num_processes) as pool:
                for c in self.dataStreams:
                    pool.map(self.collectHistoricalData(c), [])
            pool.close()

    def collectHistoricalData(self, contract):

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

    def updateData(self, reqId, bar, realtime):

        global orderId

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
                self.stockData[contractInHand].append(bar)