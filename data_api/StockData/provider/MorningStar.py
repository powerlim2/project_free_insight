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
        super(provider.Provider, self).__init__()

    def retrieve_stock_price(self, symbol, start, end):
        """
        Retrieve stock trading information from MorningStar API

        :param symbol: company stock market symbol
        :param start: "yyyy-mm-dd" format
        :param end: "yyyy-mm-dd" format
        :return: dict type
        """
        symbol = str(symbol)
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

        output = {'date':[], 'close_price':[], 'open_price':[], 'day_range_low':[], 'day_range_high':[], 'trading_volume':[]}

        total_days = len(price_data['DateIndexs'])
        for i in xrange(total_days):
            output['date'].append(self.convert_date_index(price_data['DateIndexs'][i]))
            output['close_price'].append(price_data['Datapoints'][i][0])
            output['open_price'].append(price_data['Datapoints'][i][1])
            output['day_range_low'].append(price_data['Datapoints'][i][2])
            output['day_range_high'].append(price_data['Datapoints'][i][3])
            output['trading_volume'].append(long(volume_data['Datapoints'][i] * 1000000))

        return output

    def convert_date_index(self, excel_date_index):
        """Return the balance remaining after depositing *amount*
        dollars."""
        base = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(days=excel_date_index)
        return (base+delta).strftime('%Y-%m-%d')
