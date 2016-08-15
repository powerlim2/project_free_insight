
CREATE "NameUser" insight createDB WITH PASSWORD 'insight';

CREATE USER insight WITH PASSWORD 'insight';


/**
 * pSQL way of "USE insight": change default DB to "insight"
 */
\c insight

/**
 * CREATE TABLE for storing Stock Trading Data
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
 * provide permission to 'insight' account
 */
GRANT ALL PRIVILEGES ON TABLE STOCK to insight;
