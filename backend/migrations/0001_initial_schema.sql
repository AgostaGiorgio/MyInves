CREATE TYPE currency_enum AS ENUM ('EUR', 'USD', 'AED');
CREATE TYPE asset_type_enum AS ENUM ('ETF', 'CRYPTO', 'CASH', 'GOLD', 'BANK_ACCOUNT');

CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    asset_type asset_type_enum NOT NULL,
    currency currency_enum NOT NULL
);

CREATE TABLE asset_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    record_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    quantity DECIMAL(10, 4) NOT NULL
);