CREATE TABLE exchange_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    currency currency_enum NOT NULL, 
    record_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    rate_to_eur DECIMAL(10, 4) NOT NULL,
    UNIQUE(currency, record_date)
);