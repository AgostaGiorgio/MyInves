from sqlalchemy import text, TextClause
from src.db.models.asset import Period, PERIOD_MONTHS

# Tipi tracciati a valore diretto: la lettura e' il valore posseduto, non una
# quantita' da moltiplicare per un prezzo di mercato (allineato con il frontend).
VALUE_TRACKED_SQL = "('CASH', 'BANK_ACCOUNT', 'BANK_ACCOUNT_STATIC', 'OTHER')"

NEW_ASSET = text("""
INSERT INTO assets (name, asset_type, currency, icon_base64, details)
VALUES (:name, :asset_type, :currency, :icon_base64, (:details)::jsonb)
RETURNING id
""")

UPDATE_ASSET = text("""
UPDATE assets
SET name = :name,
    asset_type = :asset_type,
    currency = :currency,
    icon_base64 = :icon_base64,
    details = (:details)::jsonb
WHERE id = :id
""")

GET_ASSET_TYPE = text("""
SELECT asset_type
FROM assets
WHERE id = :id
""")

GET_ASSET_PRICES = text("""
SELECT id, asset_id, record_date, price
FROM asset_prices
WHERE asset_id = :asset_id
ORDER BY record_date DESC
""")

NEW_ASSET_PRICE = text(f"""
INSERT INTO asset_prices (asset_id, record_date, price)
SELECT :asset_id, :record_date, :price
WHERE EXISTS (
    SELECT 1 FROM assets
    WHERE id = :asset_id AND asset_type NOT IN {VALUE_TRACKED_SQL}
)
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

NEW_ASSET_ORDER = text("""
INSERT INTO asset_orders (asset_id, order_date, side, quantity, amount_invested, fees, note)
VALUES (:asset_id, :order_date, :side, :quantity, :amount_invested, :fees, :note)
RETURNING id, order_date
""")

GET_ASSET_ORDERS = text("""
SELECT id, asset_id, order_date, side, quantity, amount_invested, fees, note
FROM asset_orders
WHERE asset_id = :asset_id
ORDER BY order_date DESC
""")

DELETE_ASSET_ORDER = text("""
DELETE FROM asset_orders
WHERE id = :id AND asset_id = :asset_id
RETURNING side, quantity, amount_invested
""")

GET_LATEST_READING = text("""
SELECT quantity, cost_price
FROM asset_readings
WHERE asset_id = :asset_id
ORDER BY record_date DESC
LIMIT 1
""")

GET_LATEST_MANUAL_READING = text("""
SELECT quantity, cost_price
FROM asset_readings
WHERE asset_id = :asset_id AND source = 'manual'
ORDER BY record_date DESC
LIMIT 1
""")

GET_ASSET_ORDERS_ASC = text("""
SELECT side, quantity, amount_invested
FROM asset_orders
WHERE asset_id = :asset_id
ORDER BY created_at ASC, id ASC
""")

DELETE_ORDER_READINGS = text("""
DELETE FROM asset_readings
WHERE asset_id = :asset_id AND source = 'order'
""")

NEW_READING_ON_DATE = text("""
INSERT INTO asset_readings (asset_id, record_date, quantity, cost_price, source)
VALUES (
    :asset_id,
    GREATEST(
        CAST(:record_date AS timestamptz),
        CURRENT_TIMESTAMP,
        COALESCE(
            (SELECT MAX(record_date) FROM asset_readings WHERE asset_id = :asset_id),
            '-infinity'::timestamptz
        ) + INTERVAL '1 microsecond'
    ),
    :quantity,
    :cost_price,
    'order'
)
""")

GET_ASSET_ICON = text("""
SELECT id, icon_base64
FROM assets
WHERE id = :id
""")

GET_MARKET_HISTORY = text("""
WITH price_ranks AS (
    SELECT
        'asset'::text AS kind,
        a.id::text AS item_id,
        a.name AS name,
        a.currency AS currency,
        a.icon_base64 AS icon_base64,
        p.record_date AS record_date,
        p.price AS value,
        ROW_NUMBER() OVER (PARTITION BY a.id ORDER BY p.record_date DESC) AS rn
    FROM assets a
    JOIN asset_prices p ON p.asset_id = a.id
),
rate_ranks AS (
    SELECT
        'rate'::text AS kind,
        e.currency AS item_id,
        e.currency AS name,
        e.currency AS currency,
        NULL::text AS icon_base64,
        e.record_date AS record_date,
        e.rate_to_eur AS value,
        ROW_NUMBER() OVER (PARTITION BY e.currency ORDER BY e.record_date DESC) AS rn
    FROM exchange_rates e
)
SELECT kind, item_id, name, currency, icon_base64, record_date, value, rn
FROM price_ranks WHERE rn <= :points
UNION ALL
SELECT kind, item_id, name, currency, icon_base64, record_date, value, rn
FROM rate_ranks WHERE rn <= :points
ORDER BY kind, name, rn DESC
""")

GET_EXCHANGE_RATES = text("""
SELECT DISTINCT ON (currency) *
FROM exchange_rates
WHERE DATE_TRUNC('month', record_date) = DATE_TRUNC('month', CURRENT_DATE)
ORDER BY currency, record_date DESC;
""")

GET_ALL_EXCHANGE_RATES = text("""
SELECT id, currency, record_date, rate_to_eur
FROM exchange_rates
ORDER BY currency, record_date DESC
""")

NEW_EXCHANGE_RATE = text("""
INSERT INTO exchange_rates (currency, record_date, rate_to_eur)
VALUES (:currency, :record_date, :rate_to_eur)
RETURNING id
""")

UPDATE_EXCHANGE_RATE = text("""
UPDATE exchange_rates
SET currency = :currency,
    record_date = :record_date,
    rate_to_eur = :rate_to_eur
WHERE id = :id
""")

DELETE_EXCHANGE_RATE = text("""
DELETE FROM exchange_rates
WHERE id = :id
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
    a.details,
    COALESCE(lp.price, 1) AS price,
    COALESCE(lp.record_date, CURRENT_DATE) AS price_date
FROM assets a
LEFT JOIN LatestPrices lp ON a.id = lp.asset_id
ORDER BY a.asset_type, a.name;
""")

GET_PORTFOLIO = text(f"""
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
        asset_id, quantity, cost_price, record_date
    FROM asset_readings
    ORDER BY asset_id, record_date DESC
),
Base AS (
    SELECT 
        a.id, 
        a.name, 
        a.asset_type, 
        at.label AS asset_label,
        a.currency, 
        COALESCE(lread.record_date, CURRENT_DATE) AS reading_date,
        COALESCE(lread.quantity, 0) AS quantity,
        lread.cost_price AS cost_price,
        CASE WHEN a.asset_type IN {VALUE_TRACKED_SQL}
             THEN 1.0 ELSE COALESCE(lp.price, 1.0) END AS unit_price,
        CASE WHEN a.currency = 'EUR' THEN 1.0
             ELSE COALESCE(lr.rate_to_eur, 1.0) END AS fx
    FROM assets a
    LEFT JOIN asset_types at ON a.asset_type = at.code
    LEFT JOIN LatestReadings lread ON a.id = lread.asset_id
    LEFT JOIN LatestPrices lp ON a.id = lp.asset_id
    LEFT JOIN LatestRates lr ON a.currency = lr.currency
)
SELECT
    id,
    name,
    asset_type,
    asset_label,
    currency,
    reading_date,
    quantity,
    cost_price,
    ROUND(quantity * unit_price * fx, 2) AS total_value_eur,
    CASE WHEN cost_price IS NOT NULL AND asset_type NOT IN {VALUE_TRACKED_SQL}
         THEN ROUND(quantity * cost_price * fx, 2) END AS cost_value_eur,
    CASE WHEN cost_price IS NOT NULL AND asset_type NOT IN {VALUE_TRACKED_SQL}
         THEN ROUND(quantity * (unit_price - cost_price) * fx, 2) END AS unrealized_pl_eur,
    CASE WHEN cost_price IS NOT NULL AND cost_price > 0 AND asset_type NOT IN {VALUE_TRACKED_SQL}
         THEN ROUND((unit_price - cost_price) / cost_price * 100, 2) END AS unrealized_pl_pct
FROM Base
ORDER BY total_value_eur DESC;
""")

NEW_READING = text("""
INSERT INTO asset_readings (asset_id, quantity, cost_price)
VALUES (:asset_id, :quantity, :cost_price)
""")

NEW_CURRENCY = text("""
INSERT INTO currencies (code, label)
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

GET_ALL_ASSETS_HISTORY = text("""
SELECT
    a.name,
    ah.record_date,
    ah.total_value_eur
FROM assets_history ah
LEFT JOIN assets a
    ON a.id = ah.asset_id
ORDER BY a.name, ah.record_date;
""")

GET_ALL_PORTFOLIO_HISTORY = text("""
SELECT record_date, total_value_eur
FROM portfolio_history
ORDER BY record_date;
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
