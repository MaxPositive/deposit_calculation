from pydantic import ValidationError
from src.models import DepositModel


def test_valid_date_format():
    deposit_data = {"date": "31.01.2023", "periods": 3, "amount": 10000, "rate": 6}
    model = DepositModel(**deposit_data)
    assert model.date == "31.01.2023"


def test_invalid_date_format():
    deposit_data = {"date": "2023-01-31", "periods": 3, "amount": 10000, "rate": 6}
    try:
        model = DepositModel(**deposit_data)
    except ValidationError as e:
        assert ("Invalid Date Format" in str(err) for err in e.errors())


def test_valid_periods():
    deposit_data = {"date": "31.01.2023", "periods": 30, "amount": 10000, "rate": 6}
    model = DepositModel(**deposit_data)
    assert model.periods == 30


def test_invalid_periods():
    deposit_data = {"date": "31.01.2023", "periods": 70, "amount": 10000, "rate": 6}
    try:
        model = DepositModel(**deposit_data)
    except ValidationError as e:
        assert ("Invalid Periods" in str(err) for err in e.errors())


def test_valid_amount():
    deposit_data = {"date": "31.01.2023", "periods": 3, "amount": 50000, "rate": 6}
    model = DepositModel(**deposit_data)
    assert model.amount == 50000


def test_invalid_amount():
    deposit_data = {"date": "31.01.2023", "periods": 3, "amount": 500, "rate": 6}
    try:
        model = DepositModel(**deposit_data)
    except ValidationError as e:
        assert ("Invalid Amount" in str(err) for err in e.errors())


def test_valid_rate():
    deposit_data = {"date": "31.01.2023", "periods": 3, "amount": 10000, "rate": 5}
    model = DepositModel(**deposit_data)
    assert model.rate == 5


def test_invalid_rate():
    deposit_data = {"date": "31.01.2023", "periods": 3, "amount": 10000, "rate": 10}
    try:
        model = DepositModel(**deposit_data)
    except ValidationError as e:
        assert ("Invalid Rate" in str(err) for err in e.errors())
