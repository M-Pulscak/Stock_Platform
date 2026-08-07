from __future__ import annotations
from db.database import Database
from domain.fundamental_metric import FundamentalMetric
from domain.save_status import SaveStatus
from models.fundamental import FundamentalRecord
from repositories.currency_repository import CurrencyRepository
from repositories.provider_repository import ProviderRepository


class FundamentalRepository:
    """
    Repository for current and historical fundamentals.
    """

    def __init__(
        self,
        db: Database,
        currency_repo: CurrencyRepository,
        provider_repo: ProviderRepository,
    ) -> None:

        self._db = db
        self._currency_repo = currency_repo
        self._provider_repo = provider_repo

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(
        self,
        record: FundamentalRecord,
    ) -> SaveStatus:
        """
        Saves one fundamental record.
        """

        raise NotImplementedError()

    def get_snapshot(
        self,
        asset_id: int,
        provider_code: str,
        metric: FundamentalMetric,
    ) -> FundamentalRecord | None:
        """
        Returns current snapshot.
        """

        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _insert_snapshot(
        self,
        record: FundamentalRecord,
    ) -> None:

        raise NotImplementedError()

    def _update_snapshot(
        self,
        record: FundamentalRecord,
    ) -> None:

        raise NotImplementedError()

    def _insert_history(
        self,
        record: FundamentalRecord,
    ) -> None:

        raise NotImplementedError()

    def _snapshot_changed(
        self,
        current: FundamentalRecord,
        new: FundamentalRecord,
    ) -> bool:

        raise NotImplementedError()