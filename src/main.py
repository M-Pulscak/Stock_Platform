from db.database import Database

from repositories.exchange_repository import ExchangeRepository
from repositories.currency_repository import CurrencyRepository
from repositories.asset_type_repository import AssetTypeRepository
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from services.yahoo import YahooService
from services.yahoo_price import YahooPriceService
from mappers.yahoo_mapper import YahooMapper
from mappers.price_mapper import PriceMapper
from importers.assets import AssetImporter
from importers.prices import PriceImporter


def main():

    ticker = "MSFT"

    with Database() as db:
        exchange_repo = ExchangeRepository(db)
        currency_repo = CurrencyRepository(db)
        asset_type_repo = AssetTypeRepository(db)
        asset_repo = AssetRepository(
            db,
            exchange_repo,
            currency_repo,
            asset_type_repo,
        )
        price_repo = PriceRepository(db)
        asset_importer = AssetImporter(
            YahooService(),
            YahooMapper(),
            asset_repo,
        )
        price_importer = PriceImporter(
            YahooPriceService(),
            PriceMapper(),
            asset_repo,
            price_repo,
        )
        asset_id = asset_importer.import_ticker(ticker)
        print(f"Imported asset_id = {asset_id}")
        imported_days = price_importer.import_ticker(ticker)
        print(f"Imported {imported_days} daily prices")


if __name__ == "__main__":
    main()
