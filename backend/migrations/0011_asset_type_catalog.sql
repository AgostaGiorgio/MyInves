-- Catalogo chiuso dei tipi: gestito via migrazioni, non piu' a runtime.
-- Aggiunge il tipo generico OTHER e rinominina GOLD in METAL (oro/argento).

INSERT INTO currencies (code, label) VALUES ('AED', 'UAE Dirham')
ON CONFLICT (code) DO NOTHING;

INSERT INTO asset_types (code, label) VALUES ('OTHER', 'Other')
ON CONFLICT (code) DO NOTHING;

-- La FK assets.asset_type e' ON UPDATE CASCADE: propaga automaticamente.
UPDATE asset_types
SET code = 'METAL', label = 'Precious metal'
WHERE code = 'GOLD';

-- I metalli esistenti diventano oro.
UPDATE assets
SET details = jsonb_build_object('metal', 'gold')
WHERE asset_type = 'METAL' AND details = '{}'::jsonb;
