STOCK_TABLE_SCHEMA = {
    'SCHEMA': {
        'SYMBOL': 'VARCHAR(20) NOT NULL',
        'TRADE_DATE': 'DATE NOT NULL',
        'CLOSE_PRICE': 'DOUBLE PRECISION',
        'OPEN_PRICE': 'DOUBLE PRECISION',
        'DAILY_LOW': 'DOUBLE PRECISION',
        'DAILY_HIGH': 'DOUBLE PRECISION',
        'TRADE_VOLUME': 'BIGINT'},
    'PRIMARY_KEY': 'SYMBOL, TRADE_DATE',
    'POSITION': ['SYMBOL', 'TRADE_DATE', 'CLOSE_PRICE', 'OPEN_PRICE', 'DAILY_LOW', 'DAILY_HIGH', 'TRADE_VOLUME']
}

