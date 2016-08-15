import psycopg2
import database


class PostgreSQL(database.DB):
    """
    Store Stock data into PostgreSQL DB

    Static:
        db_path: db access path

    Attributes:
        balance: A float tracking the current balance of the customer's account.


    Methods:
        store_stock_price:

    """
    postgre_DB = postgre_user = postgre_password = 'insight'

    def __init__(self):
        super(self.__class__, self).__init__()
        try:
            argument = "dbname='{0}' user='{1}' password='{2}' host=localhost".format(self.postgre_DB, self.postgre_user, self.postgre_password)
            self.connection = psycopg2.connect(argument)
        except:
            raise Exception("Connection Error: unable to connect to postgreSQL DB")

    def store_stock_price(self, stock_data):
        """
        retrieve stock price, volume, date, dividend data

        :param stock_data: list of dicts
        """
        if len(stock_data) == 0:
            raise Exception('InvalidInputException: provide appropriate stock data')

        query = """INSERT INTO STOCK(SYMBOL, TRADE_DATE, CLOSE_PRICE, OPEN_PRICE, DAILY_LOW, DAILY_HIGH, TRADE_VOLUME) """ \
                """VALUES (%(SYMBOL)s, %(TRADE_DATE)s, %(CLOSE_PRICE)s, %(OPEN_PRICE)s, %(DAILY_LOW)s, %(DAILY_HIGH)s, %(TRADE_VOLUME)s)"""

        cursor = self.connection.cursor()
        cursor.executemany(query, stock_data)

        self.connection.commit()
        print "Successfully inserted {0} records into STOCK table.\n".format(len(stock_data))
