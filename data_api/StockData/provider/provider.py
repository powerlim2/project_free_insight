from abc import ABCMeta, abstractmethod


class Provider(object):
    """
    Abstract Class for retrieving Stock data from provider

    Static:
        api_path: RestAPI path

    Attributes:
        balance: A float tracking the current balance of the customer's account.

    Methods:
        retrieve_stock_price:

    """
    __metaclass__ = ABCMeta

    api_path = 'put_specific_RestAPI_path_here'

    def __init__(self):
        """
        initiate the provider class
        """

    @abstractmethod
    def retrieve_stock_price(self, symbol, start, end):
        """
        retrieve stock price, volume, date, dividend data

        :param symbol:
        :param start:
        :param end:
        :return:
        """
        raise Exception('MethodNotImplementedError: ' + self.retrieve_stock_price.__name__)
