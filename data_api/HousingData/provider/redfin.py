import requests
import provider

from cookie import redfin_cookie 


# redfin search options 
base_param = {
    'market' : 'sanfrancisco',
    'num_homes' : '9000',
    'ord' : 'redfin-recommended-asc',
    'region_id' : '2673',
    'region_type' : '6',
    'v' : '8',
    'uipt' : '1',
    'status' : '1',
    'sp' : 'true',
    'sold_within_days' : '365'
}

#redfin regions (should always be lower case)
region_param = {
    'campbell' : {
        'region_id' : '2673',
        'region_type' : '6'},
    'santa clara' : {
        'region_id' : '17675',
        'region_type' : '6'},
    'west valley' : {
        'region_id' : '116902',
        'region_type' : '1'}
}

# headers to mimic a browser visit
request_headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br',
    'Accept-Language' : 'en-US,en;q=0.8,id;q=0.6,ko;q=0.4',
    'Cache-Control' : 'no-cache',
    'Connection' : 'keep-alive',
    'Host' : 'www.redfin.com',
    'Cookie' : redfin_cookie.latest_cookie,
    'Pragma' : 'no-cache',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

# redfin result columns
result_columns = ['SALE_TYPE', 'SOLD_DATE', 'PROPERTY_TYPE', 'ADDRESS', 'CITY', 'STATE', 'ZIPCODE', 'PRICE', 'BEDS', 'BATHS', 'LOCATION', 'SQFT', 'LOT_SIZE', 'YEAR_BUILT', 'DAYS_ON_MARKET', 'DOLLAR_PER_SQFT', 'HOA_MONTHLY', 'STATUS', 'NEXT_OPEN_HOUSE_START_TIME', 'NEXT_OPEN_HOUSE_END_TIME' , 'URL', 'SOURCE', 'MLS_NUM', 'FAVORITE', 'INTERESTED', 'LATITUDE', 'LONGITUDE']

# columns that we want to save
target_columns = {'SALE_TYPE', 'SOLD_DATE', 'PROPERTY_TYPE', 'ADDRESS', 'CITY', 'STATE', 'ZIPCODE', 'PRICE', 'BEDS', 'BATHS', 'SQFT', 'LOT_SIZE', 'YEAR_BUILT', 'DAYS_ON_MARKET', 'DOLLAR_PER_SQFT', 'HOA_MONTHLY', 'STATUS', 'URL', 'MLS_NUM', 'LATITUDE', 'LONGITUDE'}


class Redfin(provider.Provider):
    """
    Retrieve Stock data from MorningStar API

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.

    Methods:
        retrieve_stock_price:

    """
    search_result_api_path = 'https://www.redfin.com/stingray/api/gis-csv?al=3&sf=1,2,3,5,6,7'

    def __init__(self):
        super(self.__class__, self).__init__()

    def retrieve_search_result_by_city(self, city):
        """
        Retrieve Housing Market data for a specific city from Redfin

        :param symbol: company stock market symbol
        :return: list type
        """
        assert isinstance(city, str)
        assert city.lower() in region_param

        search_param = dict(base_param, 
                            region_id=region_param[city]['region_id'],
                            region_type=region_param[city]['region_type'])

        try:
            requested = requests.get(self.search_result_api_path, params = search_param, headers = request_headers)
            requested.raise_for_status()
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

        if not requested.content:
            raise Exception('not able to retrieve the data')

        line_count = 0
        output = []
        for line_item in requested.iter_lines():
            items = line_item.split(',')
            # null join key handling (invalid record)
            if any(join_key in {'', ' ', None} for join_key in items[3:7]): continue
            # make sure the data is complete
            if len(items) == len(result_columns):
                row_result = {}
                for i in xrange(len(items)):
                    if result_columns[i] in target_columns:
                        if items[i] == '': items[i] = None  # add null instead of blank character
                        row_result[result_columns[i]] = items[i]
                if line_count != 0:  # skip the header row
                    output.append(row_result)
                line_count += 1

        print "Successfully retrieved {0} houses for {1} from Redfin.".format(line_count, city)
        return output


def main():
    rdf = Redfin()
    data = rdf.retrieve_search_result_by_city(city = 'campbell')
    print data


if __name__ == '__main__':
    main()



