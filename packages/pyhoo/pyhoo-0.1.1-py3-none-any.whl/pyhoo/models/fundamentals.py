import enum
from dataclasses import dataclass
from typing import Sequence, TypeVar

from pyhoo.models.abc import BaseModel, OptionalFieldsModel
from pyhoo.types.fundamentals import ReportedValueDict

T = TypeVar("T")


class Frequency(enum.Enum):

    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"


@dataclass(frozen=True)
class ReportedValue(OptionalFieldsModel):

    raw: float
    fmt: str


class FundamentalsRow(BaseModel):

    dataId: int
    asOfDate: str
    periodType: str
    reportedValue: ReportedValue
    currencyCode: str

    def __init__(
        self,
        dataId: int,
        asOfDate: str,
        periodType: str,
        reportedValue: ReportedValueDict,
        currencyCode: str = "",
    ) -> None:
        self.dataId = dataId
        self.asOfDate = asOfDate
        self.periodType = periodType
        self.reportedValue = ReportedValue(**reportedValue)
        self.currencyCode = currencyCode


class FundamentalsMeta(BaseModel):

    symbol: str
    type: str

    def __init__(self, symbol: Sequence[str], type: Sequence[str]) -> None:
        self.symbol = self._get_first_element(symbol)
        self.type = self._get_first_element(type)

    @staticmethod
    def _get_first_element(sequence: Sequence[T]) -> T:
        return sequence[0]
