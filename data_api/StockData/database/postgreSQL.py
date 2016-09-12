from query.postgreSqlQuery import PostgreSqlQuery
from schema import tableSchema

import psycopg2
import database
import datetime


CURRENT_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


class PostgreSQL(database.DB):
    """
    Store Stock data into PostgreSQL DB

    Static:
        db_path: db access path
        temp_stock_table_name: the name of temporary stock table (internal use)

    Attributes:
        stock_table_query: class to generate queries to work with STOCK table in postgreSQL DB.


    Methods:
        store_stock_price:

    """
    __postgre_DB = __postgre_user = __postgre_password = 'insight'
    __temp_stock_table_name = 'TEMP_STOCK'
    __stock_table_name = 'STOCK'

    def __init__(self):
        super(self.__class__, self).__init__()

        self.stock_table_query = PostgreSqlQuery(tableSchema.STOCK_TABLE_SCHEMA)
        try:
            argument = "dbname='{0}' user='{1}' password='{2}' host=localhost".format(self.__postgre_DB, self.__postgre_user, self.__postgre_password)
            self.connection = psycopg2.connect(argument)
        except Exception, errorStack:
            print errorStack
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
        print """Successfully inserted {0} records into '{1}' table.""".format(len(stock_data), self.__stock_table_name)
        return self

    def _create_temp_stock_table(self):
        create_query = self.stock_table_query.get_create_table_statement(self.__temp_stock_table_name)
        cursor = self.connection.cursor()
        cursor.execute(create_query)
        self.connection.commit()
        return self

    def _insert_stock_data_into_temp_table(self, stock_data):
        insert_query = self.stock_table_query.get_insert_table_statement(self.__temp_stock_table_name)
        cursor = self.connection.cursor()
        cursor.executemany(insert_query, stock_data)
        cursor.execute(self.stock_table_query.get_lock_table_statement(self.__temp_stock_table_name))
        self.connection.commit()
        return self

    def _update_and_insert_temp_data(self):
        upsert_query = self.stock_table_query.get_upsert_table_statement(self.__stock_table_name, self.__temp_stock_table_name, CURRENT_DATE)
        cursor = self.connection.cursor()
        cursor.execute(upsert_query['UPDATE'])
        cursor.execute(upsert_query['INSERT'])
        self.connection.commit()
        return self

    def _delete_temp_stock_table(self):
        if not self.stock_table_query:
            raise Exception('NullClassException: stock_table_query is null!')

        query = self.stock_table_query.get_drop_table_statement(self.__temp_stock_table_name)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            return self

        except Exception, error_stack:
            print str(error_stack)
            self.connection.rollback()
            pass
