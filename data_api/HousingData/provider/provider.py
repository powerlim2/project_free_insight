from abc import ABCMeta, abstractmethod


class Provider(object):
    """
    Abstract Class for retrieving housing market data from provider

    Static:
        search_result_api_path: RestAPI path

    Methods:
        retrieve_search_result_by_city:

    """
    __metaclass__ = ABCMeta

    search_result_api_path = 'put_specific_RestAPI_path_here'

    def __init__(self):
        """
        initiate the provider class
        """

    @abstractmethod
    def retrieve_search_result_by_city(self, city):
        """
        retrieve housing market data for a specific city

        :param city:
        :return:
        """
        raise Exception('MethodNotImplementedError: ' + self.retrieve_stock_price.__name__)
