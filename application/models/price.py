from typing import Union

from iso4217 import Currency

from pydantic import BaseModel


class Price(BaseModel):
    amount: int
    currency: Currency # uses iso4217

    def __init__(self, amount: Union[float, int, str], currency_code: str):
        """
        :param amount: Is a float representation of a price. Ex: "$5.23" -> 5.23
        :param currency_code: iso4217 currency code. Ex: "USD"
        """
        currency = Currency(currency_code.upper())
        amount = self._convert_to_float(amount) * pow(10, currency.exponent)
        super().__init__(amount=amount, currency=currency)

    @staticmethod
    def _convert_to_float(value: Union[float, int, str]) -> float:
        """
        Helper function to convert input value to a float value.
        :param value: Input value to convert.
        :return: Float value.
        """
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        elif isinstance(value, str):
            return float(value.strip("$"))
        else:
            raise ValueError("Invalid input type for 'amount'")


if __name__ == '__main__':
    p = Price(amount=5.45,currency_code="USD")
    print(p.json())
