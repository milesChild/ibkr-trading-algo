from polygon.websocket.models import WebSocketMessage
from polygon import WebSocketClient
import csv


class newTrader:
    """
    Class to handle mediation of entries, exits, and RM of positions.
    """
    broker = None  # ibkr connection for trade placement
    tradeQueue = []  # Queue of trades that is filled & emptied on each loop iteration
    positions = dict()  # OrderID -> Order
    log = None  # Log that info from runtime will be stored on
    risk_manager = None  # high-authority object for risk mgmt
    strategies = None  # list of strategies that will be traded when run

    def __init__(self):
        """
        Initialize objects for each instrument-strategy pair and the Polygon websocket object.
        """
        self.connect_to_broker()
        self.log = self.init_log()
        self.__initialize_strategies()
        self.last_msg: WebSocketMessage = None
        self.socket_client = WebSocketClient(subscriptions=[
                                             "object should provide a field or a method to efficiently grab all contracts"])

    # Method that initializes a connection between this system and the wrapped ibkr api on another server
    def connect_to_broker(self):
        # TODO: Connect to the broker via an api?
        return

    # Initialize the file to which a log will be written
    def init_log(self):
        # open the file in the write mode
        f = open('ibkr-algo/model', 'w')

        return f

    # Initialize the list of strategies that the system will trade with
    def __initialize_strategies(self):
        # TODO
        return

    # Append a message to the log
    def append_to_log(self, msg):
        # create the csv writer
        writer = csv.writer(self.log)
        writer.writerow(msg)


    def start(self):
        """
        Run Polygon websocket and begin trading on new messages (public).
        """
        self.socket_client.run(self.__handle_msg)

    def __handle_msg(self, msg: WebSocketMessage):
        """
        Initialize object last_msg field to current message and run the management loop.
        :param msg: Current Polygon WebSocketMessage
        """
        self.last_msg = msg
        self.__run_loop()

    def __run_loop(self):
        """
        Run risk/portfolio management operations and enter/exit positions on new price update.
        """
        # first, check the time and either update necessary data for positions or close them
        self.__check_time()
        # second, make sure we are at healthy risk levels before continuing to trade
        self.__manage_risk()
        # third, search for positions to enter
        self.__enter_trades()
        # fourth, manage current positions
        self.__manage_positions()

    def __check_time(self):
        """
        If the time is before 9:29 then stop all systems and wait for 9:29
        If the time is 3:59 then begin closing positions and quit looking for new positions
        Otherwise do nothing
        """
        return
