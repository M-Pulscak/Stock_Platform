from db.database import Database
from services.universe_sync_service import UniverseSyncService
from services.market_import_service import MarketImportService
from utils.logger import get_logger


logger = get_logger(__name__)


def main():
    logger.info("Stock Platform started.")
    with Database() as db:
        universe_result = UniverseSyncService(db).run()
        MarketImportService(db).run(
            universe_result.tickers
        )
    logger.info("Stock Platform finished.")


if __name__ == "__main__":
    main()
