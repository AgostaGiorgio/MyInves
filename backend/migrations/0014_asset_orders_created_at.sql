-- Timestamp reale di inserimento dell'ordine: serve per replicare il ledger
-- nell'ordine cronologico corretto anche quando `order_date` (solo data)
-- coincide tra piu' ordini.
ALTER TABLE asset_orders
    ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
