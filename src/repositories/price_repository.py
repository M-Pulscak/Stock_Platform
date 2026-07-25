from db.database import Database
from models.price import Price


class PriceRepository:

    def __init__(self, db: Database):
        self._db = db

    def upsert(self, price: Price) -> None:

        sql = """
        INSERT INTO market.prices_daily
        (
            asset_id,
            trade_date,
            open,
            high,
            low,
            close,
            adjusted_close,
            volume
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )

        ON CONFLICT (asset_id, trade_date)

        DO UPDATE SET

            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            adjusted_close = EXCLUDED.adjusted_close,
            volume = EXCLUDED.volume;
        """

        self._db.execute(
            sql,
            (
                price.asset_id,
                price.trading_date,
                price.open,
                price.high,
                price.low,
                price.close,
                price.adjusted_close,
                price.volume,
            ),
        )
    