"""
Модуль представлений для веб-страниц.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict

import pandas as pd
import requests


def get_greeting(dt: datetime) -> str:
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def main_page_view(date_str: str, transactions: pd.DataFrame, user_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для главной страницы.
    :param date_str: строка с датой и временем 'YYYY-MM-DD HH:MM:SS'
    :param transactions: DataFrame с транзакциями
    :param user_settings: словарь с настройками пользователя
    :return: JSON-ответ
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(dt)
    # Фильтрация по периоду: с начала месяца по входящую дату (включительно)
    start_date = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    period_df = transactions[(transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= dt)]
    # По каждой карте
    cards = []
    for card, group in period_df.groupby("Номер карты"):
        total_spent = group["Сумма платежа"].sum()
        cashback = round(total_spent / 100, 2)
        cards.append({"last_digits": str(card), "total_spent": round(total_spent, 2), "cashback": cashback})
    # Топ-5 транзакций
    top_transactions = period_df.nlargest(5, "Сумма платежа")
    top_list = []
    for _, row in top_transactions.iterrows():
        top_list.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(row["Сумма платежа"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    # Курс валют
    currency_rates = []
    for currency in user_settings.get("user_currencies", []):
        # Здесь должен быть реальный запрос к API, пока заглушка
        rate = 75.0 if currency == "USD" else 90.0
        currency_rates.append({"currency": currency, "rate": rate})
    # Стоимость акций
    stock_prices = []
    for stock in user_settings.get("user_stocks", []):
        # Здесь должен быть реальный запрос к API, пока заглушка
        price = 100.0
        stock_prices.append({"stock": stock, "price": price})
    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_list,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
