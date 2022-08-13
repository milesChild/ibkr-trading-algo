## Class to Handle Storage of Market Data Streams from IBKR to be Used By Strategies ##
import multiprocessing
from threading import Thread 

class dataCenter:
    dataStreams = dict()
    ib = None
    timeframe = 1  # Requests only the highest granularity of data

    ## To construct a dataCenter with an interactive brokers connection object
    def __init__(self, ib, contracts):
        self.ib = ib

        for c in contracts:
            self.dataStreams[c] = []

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
        reqId += 1


