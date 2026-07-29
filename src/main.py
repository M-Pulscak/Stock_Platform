from db.database import Database
from services.asset_sync_service import AssetSyncService
from services.price_import_service import PriceImportService
from services.universe_sync_service import UniverseSyncService
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info(" ")
    logger.info("==================================================")
    logger.info("          Stock Platform spuštěna.")
    logger.info("==================================================")
    logger.info(" ")

    # -------------------------------------------------
    # STEP 1 - Universe synchronization
    # -------------------------------------------------
    logger.info("Krok 1 - Synchronizace tickerů obsažených v akciových indexech začala.")
    logger.info(" ")
    with Database() as db:
        universe_result = UniverseSyncService(db).run()
    logger.info("Krok 1 - Tickery obsažené v indexech uloženy.")
    logger.info(" ")
    # -------------------------------------------------
    # STEP 2 - Asset synchronization
    # -------------------------------------------------
    logger.info("==================================================")
    logger.info("     Krok 2 - Synchronizace tickerů začala.")
    with Database() as db:
        AssetSyncService(db).run(
            universe_result.tickers
        )
    logger.info("Krok 2 - Seznam tickerů uložen.")
    logger.info(" ")

    # -------------------------------------------------
    # STEP 3 - Price import
    # -------------------------------------------------
    logger.info("==================================================")
    logger.info("          Krok 3 - Import cen začal.")
    PriceImportService().run(
        universe_result.tickers
    )
    logger.info("Krok 3 - Import cen dokončen.")
    logger.info(" ")
    logger.info("==================================================")
    logger.info("Stock Platform ukončena.")
    logger.info("==================================================")


if __name__ == "__main__":
    main()
