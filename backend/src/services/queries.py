from sqlalchemy import text, TextClause
from src.db.models.asset import Period, PERIOD_MONTHS

NEW_ASSET = text("""
INSERT INTO assets (name, asset_type, currency, icon_base64)
VALUES (:name, :asset_type, :currency, :icon_base64)
RETURNING id
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
    a.currency, 
    lread.record_date AS reading_date,
    
    ROUND(
        lread.quantity * COALESCE(lp.price, 1.0) * CASE 
            WHEN a.currency = 'EUR' THEN 1.0
            ELSE COALESCE(lr.rate_to_eur, 1.0)
        END,
        2
    )::TEXT AS total_value_eur
    
FROM assets a
INNER JOIN LatestReadings lread ON a.id = lread.asset_id
LEFT JOIN LatestPrices lp ON a.id = lp.asset_id
LEFT JOIN LatestRates lr ON a.currency = lr.currency
ORDER BY total_value_eur DESC;
""")

NEW_READING = text("""
INSERT INTO asset_readings (asset_id, quantity)
VALUES (:asset_id, :quantity)
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