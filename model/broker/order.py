from datetime import datetime
from enum import Enum
import uuid


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

    def __init__(self, side: Side, qty: int, symbol: str, otype: OrderType, price: float):
        """
        Construct an order from the standard order components.
        """
        self.side = side
        self.qty = qty
        self.symbol = symbol
        self.otype = otype
        self.price = price

        self.id = uuid.uuid4()

    def __str__(self):
        """
        Convert order to a text-readable order format.
        """
        return f"{self.side} {self.qty} {self.symbol} @ {self.price} {self.otype}"
