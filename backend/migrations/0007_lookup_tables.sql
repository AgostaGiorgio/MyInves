CREATE TABLE currencies (
    code TEXT PRIMARY KEY,
    label TEXT
);

INSERT INTO currencies (code, label) VALUES
    ('EUR', 'Euro'),
    ('USD', 'US Dollar'),
    ('AED', 'Emirati Dirham');

CREATE TABLE asset_types (
    code TEXT PRIMARY KEY,
    label TEXT
);

INSERT INTO asset_types (code, label) VALUES
    ('ETF', 'ETF'),
    ('CRYPTO', 'Cryptocurrency'),
    ('CASH', 'Cash'),
    ('GOLD', 'Gold'),
    ('BANK_ACCOUNT', 'Bank account with interest'),
    ('BANK_ACCOUNT_STATIC', 'Static bank account');

ALTER TABLE assets ALTER COLUMN currency TYPE TEXT,
                   ALTER COLUMN asset_type TYPE TEXT;

ALTER TABLE exchange_rates ALTER COLUMN currency TYPE TEXT;

ALTER TABLE assets
    ADD CONSTRAINT fk_assets_currency FOREIGN KEY (currency) REFERENCES currencies(code) ON UPDATE CASCADE,
    ADD CONSTRAINT fk_assets_asset_type FOREIGN KEY (asset_type) REFERENCES asset_types(code) ON UPDATE CASCADE;

ALTER TABLE exchange_rates
    ADD CONSTRAINT fk_exchange_rates_currency FOREIGN KEY (currency) REFERENCES currencies(code) ON UPDATE CASCADE;

DROP TYPE IF EXISTS currency_enum;
DROP TYPE IF EXISTS asset_type_enum;
