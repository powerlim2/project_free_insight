from abc import ABCMeta, abstractmethod


class DB(object):
    """
    Abstract Class for string Stock data into DB

    Static:
        db_path: db access path

    Attributes:
        balance: A float tracking the current balance of the customer's account.

    Methods:
        store_stock_price:

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        initiate the provider class
        """

    @abstractmethod
    def get_symbols(self, exchange):
        """
        retrieve stock symbols

        :param exchange: Symbol of Stock Exchange
        """
        raise Exception('MethodNotImplementedError: ' + self.get_symbols.__name__)

    @abstractmethod
    def store_stock_price(self, stock_data):
        """
        retrieve stock price, volume, date, dividend data

        :param stock_data: store stock price, trading volume, dividend data by date
        """
        raise Exception('MethodNotImplementedError: ' + self.store_stock_price.__name__)
