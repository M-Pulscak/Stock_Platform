from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any

from domain.fundamental_metric import FundamentalMetric


@dataclass(slots=True)
class FundamentalRecord:
    """
    Represents one normalized fundamental value.

    Exactly one value field must be populated.
    """

    asset_id: int

    provider_code: str

    metric: FundamentalMetric

    numeric_value: Decimal | None = None
    text_value: str | None = None
    date_value: date | None = None
    boolean_value: bool | None = None

    currency_code: str | None = None

    as_of_date: date | None = None

    @property
    def value(self) -> Any:
        """
        Returns the populated value.
        """

        if self.numeric_value is not None:
            return self.numeric_value

        if self.text_value is not None:
            return self.text_value

        if self.date_value is not None:
            return self.date_value

        return self.boolean_value

    @property
    def value_type(self) -> str:
        """
        Returns the value type.
        """

        if self.numeric_value is not None:
            return "NUMERIC"

        if self.text_value is not None:
            return "TEXT"

        if self.date_value is not None:
            return "DATE"

        if self.boolean_value is not None:
            return "BOOLEAN"

        return "UNKNOWN"

    def validate(self) -> None:
        """
        Validates consistency of the record.
        """

        values = [
            self.numeric_value is not None,
            self.text_value is not None,
            self.date_value is not None,
            self.boolean_value is not None,
        ]

        if sum(values) != 1:
            raise ValueError(
                "Exactly one value field must be populated."
            )

        if not self.provider_code:
            raise ValueError(
                "Provider code is required."
            )

        if self.metric is None:
            raise ValueError(
                "Metric is required."
            )