import abc


# Interface representing a strategy object, which controls the parameters by which orders will be executed and data
# will be interpreted.
class IStrategy(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(clscls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)

    # Holds the logic that will be executed on each new bar for the specified period of time
    @abc.abstractmethod
    def determineEntry(self, bars, currBar):
        raise NotImplementedError

    # Sends a bracket order for profit targets and stop losses once a trade is executed
    @abc.abstractmethod
    def bracketOrder(self, parentOrderId, quantity, contract, last):
        raise NotImplementedError
