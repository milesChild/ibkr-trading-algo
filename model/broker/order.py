from datetime import datetime
from enum import Enum
import uuid

from ibapi.contract import Contract

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
    timestamp: str


    def __init__(self, side: Side, qty: int, contract: Contract, otype: OrderType, price: float):
        """
        Construct an order from the standard order components.
        """
        self.side = side
        self.qty = qty
        self.contract = contract
        self.otype = otype
        self.price = price

        self.id = uuid.uuid4()
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def __init__(self, side: Side, qty: int, position: Position):
        self.side = side
        self.qty = qty
        self.contract = position.contract
        self.positionID = position.positionID
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        """
        Convert order to a text-readable order format.
        """
        return f"{self.side} {self.qty} {self.symbol} @ {self.price} {self.otype}"

    def set_positionID(self, id):
        self.positionID = id