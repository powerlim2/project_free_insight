import datetime
import time

from StockData.StockData import StockData
from HousingData.HousingData import HousingData
"""
Title: Data Scraping API
Author: Joonhyung Lim <powerlim2@gmail.com>
"""


def run_stock_data():
    # parameters
    target_exchanges = ['NYQ', 'NMS']
    end_date = datetime.datetime.now()
    stock_end_date = end_date.strftime('%Y-%m-%d')
    stock_start_date = (end_date - datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    # workflow
    successful_retrieval = unsuccessful_retrieval = 0
    stock_data = StockData()

    for exg in target_exchanges:
        symbols = stock_data.get_symbols(exg)
        total_symbols = len(symbols)

        for num, sym in enumerate(symbols):
            time.sleep(3)  # reduce the stress to API server

            try:
                print """Retrieving Symbol: '{0}' from Exchange: '{1}' ... ({2}/{3}) """.format(sym, exg, num+1, total_symbols)
                symbol_data = stock_data.get_historical_stock_price(symbol=sym, start=stock_start_date, end=stock_end_date)
                stock_data.store_stock_price(symbol_data)
                successful_retrieval += 1

            except Exception, error_stack:
                print """\n*** pass '{0}' due to an exception! ***""".format(sym)
                print "*** detail: " + str(error_stack.message) + " ***\n"
                unsuccessful_retrieval += 1
                pass

    print """\n\nTotal {0} stock symbols retrieved successfully""".format(successful_retrieval)


def run_housing_data():
    # parameters
    target_regions = ['campbell', 'santa clara', 'west valley']

    # workflow
    successful_retrieval = unsuccessful_retrieval = 0
    housing_data = HousingData()

    # retrieve housing data from Redfin by region and save them into DB
    total_regions = len(target_regions)
    for num, region in enumerate(target_regions):
        try:
            print """Retrieving '{0}' from Redfin ({2}/{3}) """.format(region, num+1, total_regions)
            redfin_data = housing_data.retrieve_redfin_search_result_by_city(city=region)
            housing_data.store_redfin_data(redfin_data)
            successful_retrieval += 1
        except Exception, error_stack:
            print """\n*** pass '{0}' due to an exception! ***""".format(region)
            print "*** detail: " + str(error_stack.message) + " ***\n"
            unsuccessful_retrieval += 1
            pass
        time.sleep(60)  # reduce the stress to Redfin API server

    print """\n\nTotal {0} regions retrieved successfully""".format(successful_retrieval)


def main():
    run_housing_data()
    run_stock_data()


if __name__ == "__main__":
    main()
