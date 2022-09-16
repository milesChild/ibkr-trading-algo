"""
class to represent a position (internal record-keeping object)
"""
from model.broker.order import Order

global nextPositionID

class Position:
    positionID = 0  # TODO: How to set unique posIDs
    contract = None
    qty = 0
    value = 0
    strategy = None
    totalEntryIncrements = 1  # will be > 1 for scaled entries, otherwise = 1
    totalExitIncrements = 1  # will be > 1 for scaled exits, otherwise = 1
    curEntryIncrements = 0
    curExitIncrements = 0
    entries = dict()  # orderID -> order
    exits = dict()  # orderID -> order

    def __init__(self, contract, strategy, entries, exits):
        """
        Initializes a position with its:
        :param contract: the singular contract for which the position representes a stake in
        :param strategy: the strategy that was used to initialize the position
        :param entries: the total number of entries that are required to reach the final position size
        :param exits: the total number of exits that are required to totally divest from a full position
        """
        self.setPositionID()
        self.contract = contract
        self.strategy = strategy
        self.totalEntryIncrements = entries
        self.totalExitIncrements = exits

    """
    Used when creating new positions from an initializing order.
    """
    def __init__(self, order: Order):
        self.positionID = nextPositionID
        order.set_positionID(nextPositionID)
        nextPositionID += 1
        self.contract = order.contract
        self.qty = order.qty
        self.strategy = order.strategy
        self.curEntryIncrements = 1
        self.entries[order.id] = order


    # TODO: Decide whether avg, totValue, etc. will be calculated via method (available on request) or stored in a
    #       field (and continuously updated)

    # returns the average fill price for the position
    def __calc_avg(self):
        tot = 0
        for order in self.entries:
            # dont know exactly what the field is called here
            tot += (order.price * order.qty)

        return tot / self.qty

    # uses the current price of the contract for this position to update the total value of the position
    def __update_value(self, price):
        self.value = price * self.qty

    # adds an entry to the position
    def append_entry(self, order):
        # TODO: Throw error if entry increments is already maxed out??
        self.entries[order.OrderID] = order
        self.qty += order.qty
        self.curEntryIncrements += 1

    # adds an exit to the position
    def append_exit(self, order):
        # TODO: Throw error if entry increments is already maxed out??
        self.exits[order.OrderID] = order
        self.qty -= order.qty
        self.curExitIncrements += 1