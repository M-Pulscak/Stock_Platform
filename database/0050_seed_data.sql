-- ============================================================================
-- StockPlatform
-- Migration: 0050_seed_data.sql
-- Description: Seed data
-- ============================================================================

-- ============================================================================
-- ASSET TYPES
-- ============================================================================
INSERT INTO core.asset_types (name)
VALUES
    ('STOCK'),
    ('ETF'),
    ('INDEX')
ON CONFLICT (name) DO NOTHING;


-- ============================================================================
-- CURRENCIES
-- ============================================================================
INSERT INTO core.currencies (code, name, symbol)
VALUES
    ('USD', 'US Dollar', '$'),
    ('EUR', 'Euro', '€'),
    ('CZK', 'Czech Koruna', 'Kč')
ON CONFLICT (code) DO NOTHING;


-- ============================================================================
-- MARKETS
-- ============================================================================
INSERT INTO core.markets (name, country_code, timezone)
VALUES
    ('United States', 'US', 'America/New_York'),
    ('Czech Republic', 'CZ', 'Europe/Prague')
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- PROVIDERS
-- ============================================================================
INSERT INTO core.data_providers (code, name, website)
VALUES
    ('YAHOO',   'Yahoo Finance',              'https://finance.yahoo.com'),
    ('FINNHUB', 'Finnhub',                    'https://finnhub.io'),
    ('POLYGON', 'Polygon.io',                 'https://polygon.io'),
    ('FMP',     'Financial Modeling Prep',    'https://financialmodelingprep.com'),
    ('GLEIF',   'Global Legal Entity Identifier Foundation', 'https://www.gleif.org'),
    ('MANUAL',  'Manual Import',              NULL)
ON CONFLICT (code)
DO UPDATE SET
    name      = EXCLUDED.name,
    website   = EXCLUDED.website,
    is_active = TRUE;

-- ============================================================================
-- EXCHANGES
-- ============================================================================
INSERT INTO core.exchanges
(
    market_id,
    mic,
    code,
    name,
    timezone
)
VALUES
(
    (SELECT market_id FROM core.markets WHERE name = 'United States'),
    'XNAS',
    'NASDAQ',
    'Nasdaq Stock Market',
    'America/New_York'
),
(
    (SELECT market_id FROM core.markets WHERE name = 'United States'),
    'XNYS',
    'NYSE',
    'New York Stock Exchange',
    'America/New_York'
),
(
    (SELECT market_id FROM core.markets WHERE name = 'Czech Republic'),
    'XPRA',
    'PSE',
    'Prague Stock Exchange',
    'Europe/Prague'
),
(
    (SELECT market_id FROM core.markets WHERE name = 'United States'),
    'BATS',
    'CBOE',
    'Cboe BZX Exchange',
    'America/New_York'
),
(
    (SELECT market_id FROM core.markets WHERE name = 'United States'),
    'XNGM',
    'NASDAQGM',
    'Nasdaq Global Market',
    'America/New_York'
)
ON CONFLICT (mic) DO NOTHING;