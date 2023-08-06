from __future__ import annotations

import json
from typing import List, final

from mapped_collection import AbstractMappedCollection
from pydantic import BaseModel

from .errors import EmptyCurrenciesError


@final
class Currency(BaseModel):
    code: str
    scale: float
    sign: str
    default: bool

    def __str__(self) -> str:
        return self.code

    def key(self) -> str:
        return self.code


@final
class CurrencyCollection(AbstractMappedCollection[Currency]):
    def __init__(self, currencies: List[Currency]) -> None:
        """
        :raises EmptyCurrenciesError:
        """
        super().__init__(currencies)

        if not currencies:
            raise EmptyCurrenciesError

        self._default_currency = currencies[0]

        defaults = [x for x in currencies if x.default]
        if defaults:
            self._default_currency = defaults[0]

    @classmethod
    def from_json_file(cls, file_name: str) -> CurrencyCollection:
        data = json.load(open(file_name))
        return cls([Currency.parse_obj(x) for x in data])

    def default(self) -> Currency:
        return self._default_currency

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError

        return (
            self._collection == other._collection
            and self._default_currency == other._default_currency
        )
