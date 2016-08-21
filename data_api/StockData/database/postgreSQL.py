import psycopg2
import database
import datetime


CURRENT_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


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

    def get_symbols(self, exchange):
        """
        retrieve stock symbols

        :param exchange: Symbol of Stock Exchange
        """
        query = """SELECT symbol FROM SYMBOL WHERE exchange = '{0}';""".format(exchange)

        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:
            raise Exception('DataNotAvailableException: No data available for the exchange: ' + exchange)

        return [row[0] for row in rows]

    def store_stock_price(self, stock_data):
        """
        UPSERT (stock price, volume, date, dividend) data

        :param stock_data: list of dicts
        """
        if len(stock_data) == 0:
            raise Exception('InvalidInputException: provide appropriate stock data')

        self._delete_temp_stock_table()
        self._create_temp_stock_table()
        self._insert_stock_data_into_temp_table(stock_data)
        self._update_and_insert_temp_data()

        print """Successfully inserted {0} records into 'STOCK' table.""".format(len(stock_data))

    def _create_temp_stock_table(self, table_name='TEMP_STOCK'):
        create_query = """CREATE TABLE {0} (SYMBOL VARCHAR(20) NOT NULL, TRADE_DATE DATE NOT NULL, """ \
                """CLOSE_PRICE DOUBLE PRECISION, OPEN_PRICE DOUBLE PRECISION, DAILY_LOW DOUBLE PRECISION, """ \
                """DAILY_HIGH DOUBLE PRECISION, TRADE_VOLUME BIGINT, PRIMARY KEY(SYMBOL, TRADE_DATE));""".format(table_name)

        cursor = self.connection.cursor()
        cursor.execute(create_query)
        self.connection.commit()

    def _insert_stock_data_into_temp_table(self, stock_data, table_name='TEMP_STOCK'):
        import_query = """INSERT INTO {0}(SYMBOL, TRADE_DATE, CLOSE_PRICE, OPEN_PRICE, DAILY_LOW, DAILY_HIGH, TRADE_VOLUME) """ \
                       """VALUES (%(SYMBOL)s, %(TRADE_DATE)s, %(CLOSE_PRICE)s, %(OPEN_PRICE)s, %(DAILY_LOW)s, %(DAILY_HIGH)s, %(TRADE_VOLUME)s);""".format(table_name)
        locking_query = """LOCK TABLE {0} IN EXCLUSIVE MODE;""".format(table_name)

        cursor = self.connection.cursor()
        cursor.executemany(import_query, stock_data)
        cursor.execute(locking_query)
        self.connection.commit()

    def _update_and_insert_temp_data(self):
        update_query = """UPDATE STOCK SET SYMBOL = TEMP_STOCK.SYMBOL, TRADE_DATE = TEMP_STOCK.TRADE_DATE, CLOSE_PRICE = TEMP_STOCK.CLOSE_PRICE, """ \
                       """OPEN_PRICE = TEMP_STOCK.OPEN_PRICE, DAILY_LOW = TEMP_STOCK.DAILY_LOW, DAILY_HIGH = TEMP_STOCK.DAILY_HIGH, TRADE_VOLUME = TEMP_STOCK.TRADE_VOLUME, """ \
                       """LAST_UPDATE_DATE = '{0}' FROM TEMP_STOCK WHERE (STOCK.SYMBOL = TEMP_STOCK.SYMBOL) AND (STOCK.TRADE_DATE = TEMP_STOCK.TRADE_DATE);""".format(CURRENT_DATE)

        # insert the new data
        insert_query = """INSERT INTO STOCK SELECT TEMP_STOCK.SYMBOL, TEMP_STOCK.TRADE_DATE, TEMP_STOCK.CLOSE_PRICE, """ \
                       """ TEMP_STOCK.OPEN_PRICE, TEMP_STOCK.DAILY_LOW, TEMP_STOCK.DAILY_HIGH, TEMP_STOCK.TRADE_VOLUME, '{0}' FROM TEMP_STOCK """ \
                       """LEFT OUTER JOIN STOCK ON (STOCK.SYMBOL = TEMP_STOCK.SYMBOL) AND (STOCK.TRADE_DATE = TEMP_STOCK.TRADE_DATE) """ \
                       """WHERE STOCK.SYMBOL IS NULL;""".format(CURRENT_DATE)

        cursor = self.connection.cursor()
        cursor.execute(update_query)
        cursor.execute(insert_query)
        self.connection.commit()

    def _delete_temp_stock_table(self, table_name='TEMP_STOCK'):
        query = """DROP TABLE {0};""".format(table_name)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except Exception, error_stack:
            print str(error_stack)
            self.connection.rollback()
            pass

