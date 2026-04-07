-- Check row counts
SELECT COUNT(*) AS stock_rows FROM stock_data;
SELECT COUNT(*) AS market_rows FROM market_indicators;

-- Check tickers loaded
SELECT ticker, COUNT(*) AS rows_per_ticker
FROM stock_data
GROUP BY ticker
ORDER BY ticker;

-- Check date range
SELECT MIN(date) AS start_date, MAX(date) AS end_date
FROM stock_data;

-- Preview Queries
SELECT *
FROM stock_data
ORDER BY date, ticker
LIMIT 25;

SELECT *
FROM market_indicators
ORDER BY date
LIMIT 25;

--Analysis Queries
-- Prices during collapse window
SELECT date, ticker, close
FROM stock_data
WHERE date BETWEEN '2023-03-08' AND '2023-03-13'
ORDER BY ticker, date;

-- Percent drop during collapse window
SELECT
    ticker,
    MAX(close) AS max_close,
    MIN(close) AS min_close,
    ROUND(((MIN(close) - MAX(close)) / MAX(close) * 100)::numeric, 2) AS percent_drop
FROM stock_data
WHERE date BETWEEN '2023-03-08' AND '2023-03-13'
GROUP BY ticker
ORDER BY percent_drop;

-- Daily Returns
SELECT *
FROM (
    SELECT
        date,
        ticker,
        close,
        LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
        ROUND(
            (
                (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
                / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100
            )::numeric,
            2
        ) AS return_pct
    FROM stock_data
) t
WHERE prev_close IS NOT NULL
ORDER BY ticker, date;

--Volatility
SELECT
    ticker,
    ROUND(STDDEV(close)::numeric, 2) AS volatility
FROM stock_data
WHERE date BETWEEN '2023-03-01' AND '2023-03-20'
GROUP BY ticker
ORDER BY volatility DESC;

-- Macro Joins
SELECT
    s.date,
    s.ticker,
    s.close,
    m.vix,
    m.interestrate,
    m.effr,
    m.gold,
    m.oil
FROM stock_data s
JOIN market_indicators m
    ON s.date = m.date
WHERE s.ticker = 'SIVB'
ORDER BY s.date;

-- For Metabase
-- Line chart data
SELECT date, ticker, close
FROM stock_data
ORDER BY date, ticker;

-- Collapse window only
SELECT date, ticker, close
FROM stock_data
WHERE date BETWEEN '2023-03-01' AND '2023-03-20'
ORDER BY date, ticker;
