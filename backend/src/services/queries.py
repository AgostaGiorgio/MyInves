from sqlalchemy import text, TextClause
from src.db.models.asset import Period, PERIOD_MONTHS

NEW_ASSET = text("""
INSERT INTO assets (name, asset_type, currency, icon_base64)
VALUES (:name, :asset_type, :currency, :icon_base64)
RETURNING id
""")

UPDATE_ASSET = text("""
UPDATE assets
SET name = :name,
    asset_type = :asset_type,
    currency = :currency,
    icon_base64 = :icon_base64
WHERE id = :id
""")

GET_ASSET_PRICES = text("""
SELECT id, asset_id, record_date, price
FROM asset_prices
WHERE asset_id = :asset_id
ORDER BY record_date DESC
""")

NEW_ASSET_PRICE = text("""
INSERT INTO asset_prices (asset_id, record_date, price)
VALUES (:asset_id, :record_date, :price)
RETURNING id
""")

UPDATE_ASSET_PRICE = text("""
UPDATE asset_prices
SET record_date = :record_date,
    price = :price
WHERE id = :id
""")

DELETE_ASSET_PRICE = text("""
DELETE FROM asset_prices
WHERE id = :id
""")

GET_ASSET_ICON = text("""
SELECT id, icon_base64
FROM assets
WHERE id = :id
""")

GET_EXCHANGE_RATES = text("""
SELECT DISTINCT ON (currency) *
FROM exchange_rates
WHERE DATE_TRUNC('month', record_date) = DATE_TRUNC('month', CURRENT_DATE)
ORDER BY currency, record_date DESC;
""")

GET_ASSETS = text("""
WITH LatestPrices AS (
    SELECT DISTINCT ON (asset_id) 
        asset_id, 
        price,
        record_date
    FROM asset_prices
    ORDER BY asset_id, record_date DESC
)
SELECT 
    a.id, 
    a.name, 
    a.asset_type, 
    a.currency,
    a.icon_base64,
    COALESCE(lp.price, 1) AS price,
    COALESCE(lp.record_date, CURRENT_DATE) AS price_date
FROM assets a
LEFT JOIN LatestPrices lp ON a.id = lp.asset_id
ORDER BY a.asset_type, a.name;
""")

GET_PORTFOLIO = text("""
WITH LatestPrices AS (
    SELECT DISTINCT ON (asset_id) 
        asset_id, price, record_date
    FROM asset_prices
    ORDER BY asset_id, record_date DESC
),
LatestRates AS (
    SELECT DISTINCT ON (currency)
        currency, rate_to_eur, record_date
    FROM exchange_rates
    ORDER BY currency, record_date DESC
),
LatestReadings AS (
    SELECT DISTINCT ON (asset_id)
        asset_id, quantity, record_date
    FROM asset_readings
    ORDER BY asset_id, record_date DESC
)
SELECT 
    a.id, 
    a.name, 
    a.asset_type, 
    at.label AS asset_label,
    a.currency, 
    COALESCE(lread.record_date, CURRENT_DATE) AS reading_date,
    COALESCE(ROUND(lread.quantity, 2), 0) AS quantity,
    
    ROUND(
        COALESCE(lread.quantity, 0) * COALESCE(lp.price, 1.0) * CASE 
            WHEN a.currency = 'EUR' THEN 1.0
            ELSE COALESCE(lr.rate_to_eur, 1.0)
        END,
        2
    )::TEXT AS total_value_eur
    
FROM assets a
LEFT JOIN asset_types at ON a.asset_type = at.code
LEFT JOIN LatestReadings lread ON a.id = lread.asset_id
LEFT JOIN LatestPrices lp ON a.id = lp.asset_id
LEFT JOIN LatestRates lr ON a.currency = lr.currency
ORDER BY total_value_eur DESC;
""")

NEW_READING = text("""
INSERT INTO asset_readings (asset_id, quantity)
VALUES (:asset_id, :quantity)
""")

NEW_CURRENCY = text("""
INSERT INTO currencies (code, label)
VALUES (:code, :label)
""")

NEW_ASSET_TYPE = text("""
INSERT INTO asset_types (code, label)
VALUES (:code, :label)
""")

GET_CURRENCIES = text("""
SELECT code, label
FROM currencies
ORDER BY code
""")

GET_ASSET_TYPES = text("""
SELECT code, label
FROM asset_types
ORDER BY code
""")

UPDATE_CURRENCY_LABEL = text("""
UPDATE currencies
SET label = :label
WHERE code = :code
""")

UPDATE_ASSET_TYPE_LABEL = text("""
UPDATE asset_types
SET label = :label
WHERE code = :code
""")

ASSETS_HISTORY = text("""
SELECT
    a.name,
    ah.record_date,
    ah.total_value_eur
FROM assets_history ah
LEFT JOIN assets a
    ON a.id = ah.asset_id
WHERE ah.record_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 year'
ORDER BY a.name, ah.record_date;
""")

def get_portfolio_history_query(period: Period) -> tuple[TextClause, dict]:
    if period == "all":
        return text("""
        SELECT *
        FROM portfolio_history
        ORDER BY record_date
        """), {}

    months = PERIOD_MONTHS[period]

    return text("""
    SELECT *
    FROM portfolio_history
    WHERE record_date >= date_trunc('month', CURRENT_DATE) - (:months * INTERVAL '1 month')
    ORDER BY record_date
    """), {"months": months}