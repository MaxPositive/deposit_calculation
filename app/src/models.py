from datetime import datetime
from pydantic import BaseModel, field_validator


class DepositModel(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    @field_validator("date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                "Invalid Date Format. Please provide date in dd.mm.yyyy format."
            )
        return value

    @field_validator("periods")
    def validate_periods(cls, value):
        if value < 1 or value > 60:
            raise ValueError(
                "Invalid Periods. Please provide a value between 1 and 60."
            )
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if value < 10_000 or value > 3_000_000:
            raise ValueError(
                "Invalid Amount. Please provide an amount between 10,000 and 3,000,000."
            )
        return value

    @field_validator("rate")
    def validate_rate(cls, value):
        if value < 1 or value > 8:
            raise ValueError("Invalid Rate. Please provide a rate between 1 and 8.")
        return value
