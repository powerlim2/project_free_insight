
CREATE "insight" createDB WITH PASSWORD 'insight';

CREATE USER insight WITH PASSWORD 'insight';


/**
 * pSQL way of "USE insight": change default DB to "insight"
 */
\c insight

/**
 * Step 1. CREATE TABLE for Stock Symbol data
 */
CREATE TABLE SYMBOL (
	SYMBOL VARCHAR(20) NOT NULL,
	NAME VARCHAR(100),
	EXCHANGE VARCHAR(50),
	CATEGORY_NAME VARCHAR(100),
	CATEGORY_NUMBER INT,
	PRIMARY KEY(SYMBOL)
);
/**
 * Step 1.2 provide permission to 'insight' account
 */
GRANT ALL PRIVILEGES ON TABLE SYMBOL to insight;

/**
 * Step 1.3 import pre-stored default SYMBOL data into postgreSQL 'insight' DB
 * Note: change the data path to fit your local path
 */
COPY SYMBOL FROM
'~/project_free_insights/data_api/StockData/data/Symbol.csv'
delimiter ',' csv;


/**
 * Step 2.1 CREATE TABLE for storing Stock Trading Data
 */
CREATE TABLE STOCK (
   SYMBOL VARCHAR(20) NOT NULL,
   TRADE_DATE DATE NOT NULL,
   CLOSE_PRICE DOUBLE PRECISION,
   OPEN_PRICE DOUBLE PRECISION,
   DAILY_LOW DOUBLE PRECISION,
   DAILY_HIGH DOUBLE PRECISION,
   TRADE_VOLUME BIGINT,
   PRIMARY KEY(SYMBOL, TRADE_DATE)
);

/**
 * Step 2.2 provide permission to 'insight' account
 */
GRANT ALL PRIVILEGES ON TABLE STOCK to insight;


