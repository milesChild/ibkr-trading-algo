"""
class to represent a position (internal record-keeping object)
"""

class position:
    PositionID = 0  # TODO: How to set unique posIDs
    Contract = None
    Qty = 0
    Value = 0
    Strategy = None
    TotalEntryIncrements = 1  # will be > 1 for scaled entries, otherwise = 1
    TotalExitIncrements = 1  # will be > 1 for scaled exits, otherwise = 1
    CurEntryIncrements = 0
    CurExitIncrements = 0
    Entries = dict()  # orderID -> order
    Exits = dict()  # orderID -> order

    def __init__(self, contract, strategy, entries, exits):
        """
        Initializes a position with its:
        :param contract: the singular contract for which the position representes a stake in
        :param strategy: the strategy that was used to initialize the position
        :param entries: the total number of entries that are required to reach the final position size
        :param exits: the total number of exits that are required to totally divest from a full position
        """
        self.setPositionID()
        self.Contract = contract
        self.Strategy = strategy
        self.TotalEntryIncrements = entries
        self.TotalExitIncrements = exits

    # TODO: Decide whether avg, totValue, etc. will be calculated via method (available on request) or stored in a
    #       field (and continuously updated)

    # returns the average fill price for the position
    def __calc_avg(self):
        tot = 0
        for order in self.Entries:
            # dont know exactly what the field is called here
            tot += (order.price * order.qty)

        return tot / self.Qty

    # uses the current price of the contract for this position to update the total value of the position
    def __update_value(self, price):
        self.Value = price * self.Qty

    # adds an entry to the position
    def __append_entry(self, order):
        # TODO: Throw error if entry increments is already maxed out??
        self.Entries[order.OrderID] = order
        self.qty += order.qty
        self.CurEntryIncrements += 1

    # adds an exit to the position
    def __append_exit(self, order):
        # TODO: Throw error if entry increments is already maxed out??
        self.Exits[order.OrderID] = order
        self.qty -= order.qty
        self.CurExitIncrements += 1