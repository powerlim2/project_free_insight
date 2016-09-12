from provider import MorningStar
from database import postgreSQL


class StockData(object):
    """
    Get stock price, ...
    and store them into database

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.postgre_sql = postgreSQL.PostgreSQL()
        self.morning_star = MorningStar.MorningStar()

    def get_symbols(self, exchange):
        """
        Return a list of all stock symbols traded in a target stock exchange

        :param exchange:
        :return: list
        """
        return self.postgre_sql.get_symbols(exchange)

    def get_historical_stock_price(self, symbol, start, end):
        """

        :param symbol:
        :param start:
        :param end:
        :return: list of dicts
        """
        return self.morning_star.retrieve_stock_price(symbol, start, end)

    def store_stock_price(self, stock_data):
        """

        :param stock_data: (list of dicts)
        :return:
        """
        self.postgre_sql.store_stock_price(stock_data)
        return self

