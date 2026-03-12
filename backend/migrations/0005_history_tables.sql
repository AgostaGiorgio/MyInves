CREATE TABLE portfolio_history (
    record_date TIMESTAMPTZ PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
    total_value_eur DECIMAL(10,4) NOT NULL
);

CREATE TABLE assets_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    total_value_eur DECIMAL(10,4) NOT NULL
);

