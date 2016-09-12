class PostgreSqlQuery(object):
    """
    create PostgreSQL query systematically

    """
    __error_message_base_missing = "base query statement NOT found!"

    def __init__(self, schema):
        """
        initiate the PostgreSqlQuery class
        """
        if not isinstance(schema, dict):
            raise Exception('ArgumentTypeMismatchException: schema')

        self._schema = schema
        self._create_statement = None
        self._insert_statement = None
        self._update_statement = None
        self._upsert_update_statement = None
        self._upsert_insert_statement = None
        self._select_statement = None
        self._drop_statement = None
        self._lock_statement = None

    def get_create_table_statement(self, table_name):
        self._prepare_create_statement_base()
        self._prepare_create_statement_set_fields()
        return self._create_statement.format(table_name)

    def get_insert_table_statement(self, table_name):
        self._prepare_insert_statement_base()
        self._prepare_insert_statement_set_fields()
        return self._insert_statement.format(table_name)

    def get_upsert_table_statement(self, table_name, temp_table_name, current_date):
        """
        custom upsert operator: update the value if the key exists, insert otherwise.

        - see '_prepare_upsert_statement_base() method' for the output position value
        """
        self._prepare_upsert_statement_base()
        self._prepare_upsert_statement_set_fields()
        return {'UPDATE': self._upsert_update_statement.format(table_name, temp_table_name, current_date),
                'INSERT': self._upsert_insert_statement.format(table_name, temp_table_name, current_date)}

    def get_drop_table_statement(self, table_name):
        self._drop_statement = """DROP TABLE {0};""".format(table_name)
        return self._drop_statement

    def get_lock_table_statement(self, table_name):
        self._lock_statement = """LOCK TABLE {0} IN EXCLUSIVE MODE;""".format(table_name)
        return self._lock_statement

    def _prepare_create_statement_base(self):
        self._create_statement = """CREATE TABLE {0} ({1}, PRIMARY KEY({2}));"""
        return self

    def _prepare_create_statement_set_fields(self):
        if not self._create_statement:
            raise Exception(self.__error_message_base_missing)

        fields = ",".join([field_name + " " + self._schema['SCHEMA'][field_name] for field_name in self._schema['POSITION']])
        primary_key = self._schema['PRIMARY_KEY']
        self._create_statement = self._create_statement.format("{0}", fields, primary_key)
        return self

    def _prepare_insert_statement_base(self):
        self._insert_statement = """INSERT INTO {0} ({1}) VALUES ({2});"""
        return self

    def _prepare_insert_statement_set_fields(self):
        if not self._insert_statement:
            raise Exception(self.__error_message_base_missing)

        fields = self._schema['POSITION']
        field_names = ",".join(fields)
        field_values = ",".join(['%({0})s'.format(field_name) for field_name in fields])
        self._insert_statement = self._insert_statement.format("{0}", field_names, field_values)
        return self

    def _prepare_upsert_statement_base(self):
        """
        OUTPUT POSITION 0: STOCK TABLE NAME
        OUTPUT POSITION 1: TEMP TABLE NAME
        OUTPUT POSITION 2: CURRENT DATE
        """
        self._upsert_update_statement = """UPDATE {0} SET {1} FROM {2} WHERE {3};"""
        self._upsert_insert_statement = """INSERT INTO {0} SELECT {1} FROM {2} LEFT OUTER JOIN {3} ON {4} WHERE {5};"""
        return self

    def _prepare_upsert_statement_set_fields(self):
        if (not self._upsert_update_statement) or (not self._upsert_insert_statement):
            raise Exception(self.__error_message_base_missing)

        fields = self._schema['POSITION']
        primary_keys = self._schema['PRIMARY_KEY'].split(',')

        update_set_condition = ",".join(['{0}={1}.{0}'.format(field_name, '{1}') for field_name in fields] + ["LAST_UPDATE_DATE = '{2}'"])
        update_where_condition = " AND ".join(['({1}.{0}={2}.{0})'.format(primary_key.strip(), '{0}','{1}') for primary_key in primary_keys])
        self._upsert_update_statement = self._upsert_update_statement.format("{0}", update_set_condition, "{1}", update_where_condition)

        insert_select = ",".join(['{1}.{0}'.format(field_name, '{1}') for field_name in fields] + ["'{2}'"])
        insert_join_condition = update_where_condition
        insert_where_condition = "{0}.{1} IS NULL".format('{0}', primary_keys[0].strip())
        self._upsert_insert_statement = self._upsert_insert_statement.format("{0}", insert_select, "{1}", "{0}", insert_join_condition, insert_where_condition)
        return self
