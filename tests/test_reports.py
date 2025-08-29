from datetime import datetime, timedelta

import pandas as pd
import pytest

from src import reports


def make_test_df():
    today = datetime.now()
    data = [
        {
            "Дата операции": (today - timedelta(days=10)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Супермаркеты",
            "Сумма операции": 1000,
        },
        {
            "Дата операции": (today - timedelta(days=20)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Супермаркеты",
            "Сумма операции": 2000,
        },
        {
            "Дата операции": (today - timedelta(days=40)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Супермаркеты",
            "Сумма операции": 1500,
        },
        {
            "Дата операции": (today - timedelta(days=80)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Супермаркеты",
            "Сумма операции": 500,
        },
        {
            "Дата операции": (today - timedelta(days=100)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Супермаркеты",
            "Сумма операции": 300,
        },
        {
            "Дата операции": (today - timedelta(days=10)).strftime("%d.%m.%Y %H:%M:%S"),
            "Категория": "Фастфуд",
            "Сумма операции": 300,
        },
    ]
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "category,date,expected_total",
    [
        ("Супермаркеты", None, 5000),
        ("Фастфуд", None, 300),
        ("Супермаркеты", (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"), 4300),
    ],
)
def test_spending_by_category(tmp_path, monkeypatch, category, date, expected_total):
    df = make_test_df()
    monkeypatch.setattr("builtins.open", lambda *a, **kw: open(tmp_path / "dummy.json", "w", encoding="utf-8"))
    result = reports.spending_by_category(df, category, date)
    assert result["category"] == category
    assert isinstance(result["spending"], dict)
    total = sum(result["spending"].values())
    assert total == expected_total
    assert all(isinstance(k, str) for k in result["spending"].keys())


def test_spending_by_weekday(tmp_path, monkeypatch):
    df = make_test_df()
    monkeypatch.setattr("builtins.open", lambda *a, **kw: open(tmp_path / "dummy_weekday.json", "w", encoding="utf-8"))
    result = reports.spending_by_weekday(df)
    assert "spending_by_weekday" in result
    assert isinstance(result["spending_by_weekday"], dict)
    assert set(result["spending_by_weekday"].keys()).issubset(
        {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
    )
    assert all(isinstance(k, str) for k in result["spending_by_weekday"].keys())


def test_spending_by_workday(tmp_path, monkeypatch):
    df = make_test_df()
    monkeypatch.setattr("builtins.open", lambda *a, **kw: open(tmp_path / "dummy_workday.json", "w", encoding="utf-8"))
    result = reports.spending_by_workday(df)
    assert "workday_spending" in result
    assert "weekend_spending" in result
    assert isinstance(result["workday_spending"], float)
    assert isinstance(result["weekend_spending"], float)
