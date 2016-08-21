import datetime
import time

from StockData.StockData import StockData

"""
Title: Data API
Author: Joonhyung Lim <powerlim2@gmail.com>
"""

target_exchanges = ['NYQ', 'NMS']
stock_start_date = '1900-01-01'
stock_end_date = datetime.datetime.now().strftime('%Y-%m-%d')


def run_stock_data():
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
                print "*** detail: " + str(error_stack) + " ***\n"
                unsuccessful_retrieval += 1
                pass

    print """\n\nTotal {0} stock symbols retrieved successfully""".format(successful_retrieval)


def main():
    run_stock_data()


if __name__ == "__main__":
    main()
