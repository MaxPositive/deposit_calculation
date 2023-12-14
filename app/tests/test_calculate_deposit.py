import pytest
from decimal import Decimal
import httpx


@pytest.mark.asyncio
async def test_calculate_deposit():
    url = "http://localhost:8000/deposits/"
    deposit_data = {"date": "31.01.2021", "periods": 3, "amount": 10000, "rate": 6}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=deposit_data)
        assert response.status_code == 200

        result = response.json()
        assert len(result) == deposit_data["periods"]
        assert result["31.01.2021"] == Decimal("10050.00")
        assert result["28.02.2021"] == Decimal("10100.25")
        assert result["31.03.2021"] == Decimal("10150.75")


@pytest.mark.asyncio
async def test_edge_cases():
    url = "http://localhost:8000/deposits/"
    deposit_data_minimum = {
        "date": "01.01.2023",
        "periods": 1,
        "amount": 10000,
        "rate": 1,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=deposit_data_minimum)
        assert response.status_code == 200

        result = response.json()
        assert len(result) == deposit_data_minimum["periods"]
        assert result["01.01.2023"] == 10008.33

    deposit_data_maximum_rate_periods = {
        "date": "01.01.2023",
        "periods": 60,
        "amount": 50000,
        "rate": 8,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=deposit_data_maximum_rate_periods)
        assert response.status_code == 200
        result = response.json()
        assert len(result) == deposit_data_maximum_rate_periods["periods"]
        assert result["01.01.2023"] == 50333.33
        assert result["31.12.2027"] == 74492.29

    deposit_data_max = {
        "date": "01.01.2023",
        "periods": 60,
        "amount": 3_000_000,
        "rate": 8,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=deposit_data_max)
        assert response.status_code == 200
        result = response.json()
        assert len(result) == deposit_data_max["periods"]
        assert result["01.01.2023"] == 3020000.0
        assert result["31.12.2027"] == 4469537.12


@pytest.mark.asyncio
async def test_leap_year():
    url = "http://localhost:8000/deposits/"
    deposit_data_leap_year = {
        "date": "29.02.2024",
        "periods": 2,
        "amount": 10000,
        "rate": 2,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=deposit_data_leap_year)
        assert response.status_code == 200
        result = response.json()
        assert len(result) == deposit_data_leap_year["periods"]
        assert result["29.02.2024"] == 10016.67
        assert result["31.03.2024"] == 10033.36
