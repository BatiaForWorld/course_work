import pandas as pd
import pytest

from src.views import main_page_view


@pytest.mark.parametrize(
    "date_str,expected_greeting,expected_cards",
    [
        ("2025-08-20 18:00:00", "Добрый вечер", 1),
        ("2025-08-01 10:00:00", "Доброе утро", 1),
        ("2025-08-15 12:00:00", "Добрый день", 1),
        ("2025-08-01 02:00:00", "Доброй ночи", 0),
    ],
)
def test_main_page_view(date_str, expected_greeting, expected_cards):
    data = [
        {
            "Дата операции": "2025-08-01 10:00:00",
            "Номер карты": "1234",
            "Сумма платежа": 1000,
            "Категория": "Супермаркеты",
            "Описание": "Покупка",
        },
        {
            "Дата операции": "2025-08-15 12:00:00",
            "Номер карты": "1234",
            "Сумма платежа": 500,
            "Категория": "Фастфуд",
            "Описание": "Обед",
        },
        {
            "Дата операция": "2025-08-20 18:00:00",
            "Номер карты": "5678",
            "Сумма платежа": 2000,
            "Категория": "Супермаркеты",
            "Описание": "Покупка",
        },
    ]
    df = pd.DataFrame(data)
    user_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}
    result = main_page_view(date_str, df, user_settings)
    assert result["greeting"] == expected_greeting
    assert len(result["cards"]) == expected_cards
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["stock_prices"][0]["stock"] == "AAPL"
