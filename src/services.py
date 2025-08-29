"""
Модуль сервисов для анализа транзакций.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List


def profitable_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Анализ выгодных категорий повышенного кешбэка за указанный месяц и год.
    :param data: список транзакций
    :param year: год
    :param month: месяц
    :return: JSON с анализом кешбэка по категориям
    """
    logging.info(f"Анализ кешбэка за {year}-{month}")
    result = {}
    for item in data:
        date = datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if date.year == year and date.month == month:
            category = item["Категория"]
            cashback = float(item.get("Кешбэк", 0))
            result[category] = result.get(category, 0) + cashback
    # Округление
    for k in result:
        result[k] = round(result[k], 2)
    return result
