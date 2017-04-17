REDFIN_TABLE_SCHEMA = {
    'SCHEMA': {
        'SALE_TYPE': 'VARCHAR(50)',
        'SOLD_DATE': 'DATE',
        'PROPERTY_TYPE': 'VARCHAR(50)',
        'ADDRESS': 'VARCHAR(100) NOT NULL',
        'CITY': 'VARCHAR(50) NOT NULL',
        'STATE': 'VARCHAR(50) NOT NULL',
        'ZIPCODE': 'BIGINT',
        'PRICE': 'BIGINT',
        'BEDS': 'BIGINT',
        'BATHS': 'DOUBLE PRECISION',
        'SQFT': 'BIGINT',
        'LOT_SIZE': 'BIGINT',
        'YEAR_BUILT': 'BIGINT',
        'DAYS_ON_MARKET': 'BIGINT',
        'DOLLAR_PER_SQFT': 'BIGINT',
        'HOA_MONTHLY': 'BIGINT',
        'STATUS': 'VARCHAR(50)',
        'URL': 'VARCHAR(100)',
        'MLS_NUM': 'VARCHAR(50)',
        'LATITUDE': 'DOUBLE PRECISION',
        'LONGITUDE': 'DOUBLE PRECISION'},
    'PRIMARY_KEY': 'ADDRESS, CITY, STATE, ZIPCODE',
    'POSITION': ['SALE_TYPE', 'SOLD_DATE', 'PROPERTY_TYPE', 'ADDRESS', 'CITY', 'STATE', 'ZIPCODE', 'PRICE', 'BEDS', 'BATHS', 'SQFT', 'LOT_SIZE', 'YEAR_BUILT', 'DAYS_ON_MARKET', 'DOLLAR_PER_SQFT', 'HOA_MONTHLY', 'STATUS', 'URL', 'MLS_NUM', 'LATITUDE', 'LONGITUDE']
}
