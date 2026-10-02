-- Distingue le letture generate dagli ordini (source='order') da quelle
-- inserite manualmente (source='manual'). Serve per ricalcolare esattamente
-- la posizione quando un ordine viene eliminato (replay del ledger).
ALTER TABLE asset_readings
    ADD COLUMN source TEXT NOT NULL DEFAULT 'manual';

ALTER TABLE asset_readings
    ADD CONSTRAINT asset_readings_source_check CHECK (source IN ('manual', 'order'));
