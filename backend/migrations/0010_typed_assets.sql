-- Asset tipizzati: metadati per tipo, costo di carico e storico denormalizzato.
-- Tutte le modifiche sono additive e retro-compatibili con i dati esistenti.

ALTER TABLE assets
    ADD COLUMN details JSONB NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE asset_readings
    ADD COLUMN cost_price DECIMAL(18,8);

ALTER TABLE assets_history
    ADD COLUMN asset_type TEXT;

-- Amplia la precisione per prezzi/quantita' di asset con valori molto piccoli
-- (es. crypto micro-priced). I valori esistenti rientrano tranquillamente.
ALTER TABLE asset_prices
    ALTER COLUMN price TYPE DECIMAL(18,8);

ALTER TABLE asset_readings
    ALTER COLUMN quantity TYPE DECIMAL(18,8);

-- Backfill del tipo nello storico esistente.
UPDATE assets_history ah
SET asset_type = a.asset_type
FROM assets a
WHERE a.id = ah.asset_id;
