from db.database import Database
from services.asset_sync_service import AssetSyncService
from services.price_import_service import PriceImportService
from services.universe_sync_service import UniverseSyncService
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("==================================================")
    logger.info("Stock Platform started.")
    logger.info("==================================================")

    # -------------------------------------------------
    # STEP 1 - Universe synchronization
    # -------------------------------------------------
    logger.info("STEP 1 - Universe synchronization started.")
    with Database() as db:
        universe_result = UniverseSyncService(db).run()
    logger.info("STEP 1 - Universe synchronization committed.")

    # -------------------------------------------------
    # STEP 2 - Asset synchronization
    # -------------------------------------------------
    logger.info("STEP 2 - Asset synchronization started.")
    with Database() as db:
        AssetSyncService(db).run(
            universe_result.tickers
        )
    logger.info("STEP 2 - Asset synchronization committed.")

    # -------------------------------------------------
    # STEP 3 - Price import
    # -------------------------------------------------
    logger.info("STEP 3 - Price import started.")
    PriceImportService().run(
        universe_result.tickers
    )
    logger.info("STEP 3 - Price import finished.")
    logger.info("==================================================")
    logger.info("Stock Platform finished.")
    logger.info("==================================================")


if __name__ == "__main__":
    main()
