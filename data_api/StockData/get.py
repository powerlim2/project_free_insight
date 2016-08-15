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

    def get_historical_stock_price(self, symbol, start, end):
        """

        :param symbol:
        :param start:
        :param end:
        :return: list of dicts
        """
        return self.morning_star.retrieve_stock_price(symbol, start, end)

    def getStockPrice(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance

    def store_stock_price(self, stock_data):
        """

        :param stock_data: (list of dicts)
        :return:
        """
        self.postgre_sql.store_stock_price(stock_data)


def main():
    print 'Test: Stock Data Retrieving\n'

    stock_data = StockData()

    # Check for "get_historical_stock_price"
    company_symbol = 'LNKD'
    start_date = '2000-08-01'
    end_date = '2016-08-13'

    symbol_data = stock_data.get_historical_stock_price(symbol=company_symbol, start=start_date, end=end_date)
    stock_data.store_stock_price(symbol_data)

if __name__ == "__main__":
    main()