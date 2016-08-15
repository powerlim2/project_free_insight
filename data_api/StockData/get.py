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
        self.postgre_sql = ''
        self.morning_star = MorningStar.MorningStar()

    def get_historical_stock_price(self, symbol, start, end):
        """

        :param symbol:
        :param start:
        :param end:
        :return:
        """

        return self.morning_star.retrieve_stock_price(symbol, start, end)

    def getStockPrice(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance

    def updateStockPrice(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance


def main():
    print 'Test: Stock Data Retrieving\n'

    stock_data = StockData()

    # Check for "get_historical_stock_price"
    company_symbol = 'LNKD'
    start_date = '2016-08-01'
    end_date = '2016-08-13'

    print stock_data.get_historical_stock_price(symbol=company_symbol, start=start_date, end=end_date)


if __name__ == "__main__":
    main()