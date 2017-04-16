from abc import ABCMeta, abstractmethod


class HousingDB(object):
    """
    Abstract Class for storing Housing data into DB

    Static:
        db_path: db access path

    Methods:
        store_stock_price:

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        initiate the provider class
        """

    @abstractmethod
    def store_redfin_data(self, housing_data):
        """
        store the retrieved Redfin data into DB

        :param housing_data: 
        """
        raise Exception('MethodNotImplementedError: ' + self.store_stock_price.__name__)
