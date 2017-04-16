import requests
import urllib
import datetime
import provider
import xml.etree.ElementTree as ET


# fetch ZWSID
with open('../key/Zillow', 'r') as z_key:
     zswid = z_key.read()


class Zillow():
    """
    Retrieve Stock data from MorningStar API

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.

    Methods:
        retrieve_stock_price:

    """
    search_result_api_path = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=%s' % zswid

    def __init__(self):
        # super(self.__class__, self).__init__()
        pass

    def retrieve_search_result(self, address, citystatezip):
        """
        Retrieve stock trading information from MorningStar API

        :param symbol: company stock market symbol
        :param start: "yyyy-mm-dd" format
        :param end: "yyyy-mm-dd" format
        :return: dict type
        """
        assert all(var is not None for var in (address, citystatezip))  # param must be not null

        params = {'address' : address,
                  'citystatezip' : citystatezip}
        
        requested = requests.get(self.search_result_api_path, params = params)
        requested.raise_for_status()

        if not requested.text:
            raise Exception('not able to retrieve the data')

        res = ET.fromstring(requested.text)

        # price_data = res['PriceDataList'][0]
        # volume_data = res['VolumeList']
        # total_days = len(price_data['DateIndexs'])

        # output = []
        # for i in xrange(total_days):
        #     output.append({
        #         'SYMBOL': symbol,
        #         'TRADE_DATE': self.convert_date_index(price_data['DateIndexs'][i]),
        #         'CLOSE_PRICE': price_data['Datapoints'][i][0],
        #         'OPEN_PRICE': price_data['Datapoints'][i][1],
        #         'DAILY_LOW': price_data['Datapoints'][i][2],
        #         'DAILY_HIGH': price_data['Datapoints'][i][3],
        #         'TRADE_VOLUME': long(volume_data['Datapoints'][i] * 1000000)
        #     })

        # print "Successfully retrieved {0} records from MorningStar.".format(total_days)
        return res

    def convert_date_index(self, excel_date_index):
        """
        Return the balance remaining after depositing *amount* dollars.
        """
        base = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(days=excel_date_index)
        return (base+delta).strftime('%Y-%m-%d')


def main():
    zillow = Zillow()
    data = zillow.retrieve_search_result(address='45 Colleen Ave', citystatezip='Campbell, CA')
    for child in data:
        print child.tag, child.attrib


if __name__ == '__main__':
    main()



