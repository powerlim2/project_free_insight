from provider import redfin
from database import postgreSQL


class HousingData(object):
    """
    Get housing data and store them into database

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self):
        self.postgre_sql = postgreSQL.PostgreSQL()
        self.redfin = redfin.Redfin()

    def retrieve_redfin_search_result_by_city(self, city):
        """

        :param city:
        :return: list of dicts
        """
        return self.redfin.retrieve_search_result_by_city(city)

    def store_redfin_data(self, housing_data):
        """

        :param housing_data: (list of dicts)
        :return:
        """
        self.postgre_sql.store_redfin_data(housing_data)
        return self

