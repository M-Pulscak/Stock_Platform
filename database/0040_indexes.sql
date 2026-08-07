CREATE INDEX ix_prices_asset_date
    ON market.prices_daily(asset_id, trade_date DESC);

CREATE INDEX ix_assets_ticker
    ON core.assets(ticker);

CREATE INDEX idx_fundamentals_asset
    ON market.fundamentals (asset_id);

CREATE INDEX idx_fundamentals_metric
    ON market.fundamentals (metric_code);

CREATE INDEX idx_fundamentals_provider
    ON market.fundamentals (provider_id);

CREATE INDEX idx_fundamentals_asset_metric
    ON market.fundamentals (asset_id, metric_code);


-- ============================================================================
-- FUNDAMENTAL HISTORY
-- ============================================================================

CREATE INDEX idx_fundamental_history_asset
    ON market.fundamental_history (asset_id);

CREATE INDEX idx_fundamental_history_metric
    ON market.fundamental_history (metric_code);

CREATE INDEX idx_fundamental_history_provider
    ON market.fundamental_history (provider_id);

CREATE INDEX idx_fundamental_history_asset_metric_date
    ON market.fundamental_history (
        asset_id,
        metric_code,
        as_of_date DESC
    );