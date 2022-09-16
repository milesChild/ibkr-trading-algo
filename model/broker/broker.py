from abc import abstractmethod, ABC
from enum import Enum
from model.broker.order import Order
import order

class Broker(ABC):
    """
    Abstract class representing a set of Broker tools.
    """

    @abstractmethod
    def submit_order(self, order: Order):
        """
        Submit the given order to a broker.
        """
        pass

    @abstractmethod
    def get_cash(self):
        """
        Get total cash available in account with the broker.
        """
        pass

    @abstractmethod
    def get_account_value(self):
        """
        Get total value of all cash and positions in the broker account.
        """
        pass

    @abstractmethod
    def get_position(self, symbol: str):
        """
        Get the total position size on a specific symbol from the broker.
        """
        pass


class IBKR(Broker):
    """
    IBKR implementation of the Broker class.
    """

    class Endpoint(Enum):
        SUBMIT = "/submit"
        CASH = "/cash"
        VALUE = "/value"
        POSITION = "/position"

    base_url = ""

    def __send_request(endpoint: Endpoint, type: str, params: dict = None):
        # check order type and place request using requests api
        pass

    def submit_order(self, order: Order):
        return super().submit_order(order)

    def get_cash(self):
        return super().get_cash()

    def get_account_value(self):
        return super().get_account_value()

    def get_position(self, symbol: str):
        return super().get_position(symbol)
