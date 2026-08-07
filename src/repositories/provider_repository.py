from db.database import Database
from repositories.base.reference_repository import ReferenceRepository


class ProviderRepository(ReferenceRepository):
    """
    Repository for core.data_providers.
    """

    def __init__(self, db: Database):
        super().__init__(
            db=db,
            table="core.data_providers",
            id_column="provider_id",
            key_column="code",
        )
