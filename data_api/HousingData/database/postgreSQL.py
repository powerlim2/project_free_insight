from query.postgreSqlQuery import PostgreSqlQuery
from schema import tableSchema

import psycopg2
import database
import datetime


CURRENT_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


class PostgreSQL(database.HousingDB):
    """
    Store Stock data into PostgreSQL DB

    Static:
        db_path: db access path
        temp_stock_table_name: the name of temporary stock table (internal use)

    Attributes:
        redfin_table_query: class to generate queries to work with STOCK table in postgreSQL DB.


    Methods:
        store_redfin_data:

    """
    __postgre_DB = __postgre_user = __postgre_password = 'insight'
    __temp_redfin_table_name = 'TEMP_REDFIN'
    __redfin_table_name = 'REDFIN'

    def __init__(self):
        super(self.__class__, self).__init__()

        self.table_query = {
            self.__redfin_table_name : PostgreSqlQuery(tableSchema.REDFIN_TABLE_SCHEMA)
        }
        try:
            argument = "dbname='{0}' user='{1}' password='{2}' host=localhost".format(self.__postgre_DB, self.__postgre_user, self.__postgre_password)
            self.connection = psycopg2.connect(argument)
        except Exception, errorStack:
            print errorStack
            raise Exception("Connection Error: unable to connect to postgreSQL DB")

    def store_redfin_data(self, housing_data):
        """
        UPSERT (stock price, volume, date, dividend) data

        :param stock_data: list of dicts
        """
        product = self.__redfin_table_name

        if len(housing_data) == 0:
            raise Exception('InvalidInputException: provide appropriate redfin data')

        self._delete_temp_table(product)
        self._create_temp_table(product)
        self._insert_housing_data_into_temp_table(product, housing_data)
        self._update_and_insert_temp_data(product)
        print """Successfully inserted {0} records into '{1}' table.""".format(len(housing_data), self.__redfin_table_name)
        return self

    def _create_temp_table(self, product):
        assert product in self.table_query
        create_query = self.table_query[product].get_create_table_statement(self.__temp_redfin_table_name)
        cursor = self.connection.cursor()
        cursor.execute(create_query)
        self.connection.commit()
        return self

    def _insert_housing_data_into_temp_table(self, product, housing_data):
        assert product in self.table_query
        insert_query = self.table_query[product].get_insert_table_statement(self.__temp_redfin_table_name)
        cursor = self.connection.cursor()
        cursor.executemany(insert_query, housing_data)
        cursor.execute(self.table_query[product].get_lock_table_statement(self.__temp_redfin_table_name))
        self.connection.commit()
        return self

    def _update_and_insert_temp_data(self, product):
        assert product in self.table_query
        upsert_query = self.table_query[product].get_upsert_table_statement(self.__redfin_table_name, self.__temp_redfin_table_name, CURRENT_DATE)
        cursor = self.connection.cursor()
        cursor.execute(upsert_query['UPDATE'])
        cursor.execute(upsert_query['INSERT'])
        self.connection.commit()
        return self

    def _delete_temp_table(self, product):
        assert product in self.table_query
        if not self.table_query[product]:
            raise Exception('NullClassException: table_query is null!')

        query = self.table_query[product].get_drop_table_statement(self.__temp_redfin_table_name)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            return self

        except Exception, error_stack:
            print str(error_stack)
            self.connection.rollback()
            pass
