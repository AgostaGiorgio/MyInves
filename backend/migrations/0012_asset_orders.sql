-- Registro degli ordini (acquisti/vendite) per gli asset a posizione
-- (ETF, CRYPTO, METAL). Ogni ordine aggiorna la lettura della posizione con
-- il nuovo costo medio pesato.

CREATE TABLE asset_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    order_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    side TEXT NOT NULL DEFAULT 'BUY',
    quantity DECIMAL(18,8) NOT NULL,
    amount_invested DECIMAL(18,8) NOT NULL,
    fees DECIMAL(18,8) NOT NULL DEFAULT 0,
    note TEXT
);

CREATE INDEX idx_asset_orders_asset_date ON asset_orders (asset_id, order_date DESC);
