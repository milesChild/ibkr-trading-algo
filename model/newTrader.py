from polygon.websocket.models import WebSocketMessage
from polygon import WebSocketClient
import csv


class newTrader:
    """
    Class to handle mediation of entries, exits, and RM of positions.
    """
    broker = None  # ibkr connection for trade placement
    tradeQueue = []  # Queue of trades that is filled & emptied on each loop iteration
    positions = dict()  # PositionID -> Position
    log = None  # Log that info from runtime will be stored on
    risk_manager = None  # high-authority object for risk mgmt
    strategies = None  # list of strategies that will be traded when run

    def __init__(self):
        """
        Initialize objects for each instrument-strategy pair and the Polygon websocket object.
        TODO: add code to initialize risk management operation
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
        # is a broker connection method what we want, or do we want a package in this repo that provides the tools to submit orders to our EC2 API?
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
        self.socket_client.connect(self.__handle_msg)

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
        # third, search for positions to enter (these orders are appended to self.tradeQueue)
        self.__enter_trades()
        # fourth, manage current positions (these orders are appended to self.tradeQueue)
        self.__manage_positions()
        # lastly, empty the queue and reiterate thru the loop
        self.__empty_queue()

    def __check_time(self):
        """
        If the time is before 9:29 then stop all systems and wait for 9:29
        If the time is 3:59 then begin closing positions and quit looking for new positions
        Otherwise do nothing
        """
        return

    def __manage_risk(self):
        # TODO: Use a rm object to determine whether positions need to be liquidated/trading needs to stop
        return

    """
    Empty the order queue and transmit orders one-by-one to ibkr
    """
    def __empty_queue(self):
        for order in self.tradeQueue:
            # This will require refinement of parameters passed... see old model for examples
            self.broker.transmitOrder(order)
            # update position information based on the order that was just submitted

    """
    Find positions to enter by consulting strategies and accumulating orders.
    """
    def __enter_trades(self):
        # TODO: Figure out how we provide data to these trades
        for strategy in self.strategies:
            self.tradeQueue.append(strategy.__enter_trades())

    """
    Manage open positions.
      - Determine if exits should be made for open positions
      - Continue filling scaled-entries and scaled-exits
    Any qualified order that results from strategy consultation is appended to the tradeQueue and emptied on 
    each iteration.
    """
    def __manage_positions(self):
        # TODO: Figure out how we provide data to these trades
        for strategy in self.strategies:
            respective_positions = [sub[strategy] for sub in self.positions]  # TODO: Check this line
            self.tradeQueue.append(strategy.__manage_positions(respective_positions))

    """
    To add a new position to the list of active positions
    """
    def __add_position(self, position):
        self.positions[position.PositionID] = position

    """
    Updates the status/parameters of a position based on a transmitted order
    """
    def __update_position(self, order):
        # TODO:
        return