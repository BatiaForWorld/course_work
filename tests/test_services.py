import pytest

from src.services import profitable_cashback_categories


@pytest.mark.parametrize(
    "year,month,expected_s,expected_f",
    [
        (2025, 8, 30, 5),
        (2025, 7, 15, 0),
    ],
)
def test_profitable_cashback_categories(year, month, expected_s, expected_f):
    data = [
        {"Дата операции": "01.08.2025 10:00:00", "Категория": "Супермаркеты", "Кешбэк": 10},
        {"Дата операции": "15.08.2025 12:00:00", "Категория": "Фастфуд", "Кешбэк": 5},
        {"Дата операции": "20.08.2025 18:00:00", "Категория": "Супермаркеты", "Кешбэк": 20},
        {"Дата операции": "05.07.2025 10:00:00", "Категория": "Супермаркеты", "Кешбэк": 15},
    ]
    result = profitable_cashback_categories(data, year, month)
    assert result.get("Супермаркеты", 0) == expected_s
    assert result.get("Фастфуд", 0) == expected_f
