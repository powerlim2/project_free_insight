import requests
import datetime
import provider


class MorningStar(provider.Provider):
    """
    Retrieve Stock data from MorningStar API

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.

    Methods:
        retrieve_stock_price:

    """
    api_path = 'http://globalquote.morningstar.com/globalcomponent/RealtimeHistoricalStockData.ashx?'

    def __init__(self):
        super(self.__class__, self).__init__()

    def retrieve_stock_price(self, symbol, start, end):
        """
        Retrieve stock trading information from MorningStar API

        :param symbol: company stock market symbol
        :param start: "yyyy-mm-dd" format
        :param end: "yyyy-mm-dd" format
        :return: dict type
        """
        symbol = str(symbol).upper()
        argument_line = 'ticker={0}' \
                        '&showVol=true&dtype=his&f=d&curry=USD&' \
                        'range={1}|{2}' \
                        '&isD=true&isS=true&hasF=true&ProdCode=DIRECT'.format(symbol, start, end)
        requested = requests.get(self.api_path + argument_line)
        requested.raise_for_status()

        if not requested.json():
            raise Exception('not able to retrieve the data')

        res = dict(requested.json())
        price_data = res['PriceDataList'][0]
        volume_data = res['VolumeList']
        total_days = len(price_data['DateIndexs'])

        output = []
        for i in xrange(total_days):
            output.append({
                'SYMBOL': symbol,
                'TRADE_DATE': self.convert_date_index(price_data['DateIndexs'][i]),
                'CLOSE_PRICE': price_data['Datapoints'][i][0],
                'OPEN_PRICE': price_data['Datapoints'][i][1],
                'DAILY_LOW': price_data['Datapoints'][i][2],
                'DAILY_HIGH': price_data['Datapoints'][i][3],
                'TRADE_VOLUME': long(volume_data['Datapoints'][i] * 1000000)
            })

        print "Successfully retrieved {0} records from MorningStar.\n".format(total_days)
        return output

    def convert_date_index(self, excel_date_index):
        """Return the balance remaining after depositing *amount*
        dollars."""
        base = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(days=excel_date_index)
        return (base+delta).strftime('%Y-%m-%d')
