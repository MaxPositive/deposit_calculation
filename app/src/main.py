from typing import Annotated
from datetime import datetime
from fastapi import FastAPI, status, Body, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from models import DepositModel
from decimal import Decimal
from dateutil.relativedelta import relativedelta

app = FastAPI()


def calculate_date(start_date: str, periods: int) -> str:
    """
    Calculate next date
    :param start_date: first date
    :param periods: number of periods
    :return: date of next period
    """
    current_date = datetime.strptime(start_date, "%d.%m.%Y")
    new_date = current_date + relativedelta(months=periods)
    return new_date.strftime("%d.%m.%Y")


def calculate_deposit(deposit: DepositModel) -> dict[str, float]:
    """
    Calculate deposits
    :param deposit: DepositData
    :return: dictionary with date and amount for each period
    """
    result = {}
    current_amount = Decimal(deposit.amount)
    current_date = datetime.strptime(deposit.date, "%d.%m.%Y")
    monthly_rate = Decimal(1 + deposit.rate / 12 / 100)
    current_amount *= monthly_rate
    result[current_date.strftime("%d.%m.%Y")] = float(round(current_amount, 2))
    for period in range(1, deposit.periods):
        current_date = calculate_date(deposit.date, period)
        current_amount *= monthly_rate
        result[current_date] = float(round(current_amount, 2))
    return result


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_message = {"error": exc.errors()[0]["msg"]}
    return JSONResponse(content=error_message, status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/deposits/", status_code=status.HTTP_200_OK)
async def create_deposit(
    deposit: Annotated[
        DepositModel,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "Valid example with 3 periods.",
                    "value": {
                        "date": "31.01.2023",
                        "periods": 3,
                        "amount": 10000,
                        "rate": 6,
                    },
                },
                "extra": {
                    "summary": "A extra example",
                    "description": "Valid example with 60 periods, rate 8, amount 3000000",
                    "value": {
                        "date": "31.01.2021",
                        "periods": 60,
                        "amount": 3000000,
                        "rate": 8,
                    },
                },
                "invalid": {
                    "summary": "An invalid example with amount > 3000000",
                    "description": "Invalid example that gonna throw http 400 exception.",
                    "value": {
                        "date": "29.02.2024",
                        "periods": 2,
                        "amount": 30000000,
                        "rate": 2,
                    },
                },
            }
        ),
    ],
) -> dict[str, float]:
    result = calculate_deposit(deposit)
    return result
