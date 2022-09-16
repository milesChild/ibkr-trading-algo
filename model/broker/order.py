from datetime import datetime
from enum import Enum
import uuid

from model.broker.position import Position


class Side(Enum):
    """
    Enumerated type for order sides.
    """
    BUY = "BUY"
    SELL = "SELL"
    SELL_SHORT = "SELL_SHORT"


class OrderType(Enum):
    """
    Enumerated type for order types.
    """
    LIMIT = "LIMIT"
    MARKET = "MKT"


class Order:
    """
    Class defining an order to be placed.
    """
    side: Side
    qty: int
    contract: Contract
    fillPrice: float
    orderID: int
    positionID: int


    def __init__(self, side: Side, qty: int, contract: contract, otype: OrderType, price: float):
        """
        Construct an order from the standard order components.
        """
        self.side = side
        self.qty = qty
        self.symbol = symbol
        self.otype = otype
        self.price = price

        self.id = uuid.uuid4()

    def __init__(self, side: Side, qty: int, position: Position):
        self.side = side
        self.qty = qty
        self.symbol = position.contract.symbol
        self.positionID = position.positionID

    def __str__(self):
        """
        Convert order to a text-readable order format.
        """
        return f"{self.side} {self.qty} {self.symbol} @ {self.price} {self.otype}"

    def set_positionID(self, id):
        self.positionID = id