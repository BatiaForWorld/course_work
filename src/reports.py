"""
Модуль для формирования отчетов по транзакциям.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional

import pandas as pd


def save_report_to_file(func: Callable) -> Callable:
    """
    Декоратор для записи результата функции-отчета в файл с именем по умолчанию.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        import os

        os.makedirs("report_spending", exist_ok=True)
        filename = os.path.join(
            "report_spending", f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logging.info(f"Отчет сохранен в файл {filename}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении отчета: {e}")
        return result

    return wrapper


@save_report_to_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """
    Возвращает траты по заданной категории за последние три месяца от переданной даты.
    :param transactions: DataFrame с транзакциями
    :param category: Название категории
    :param date: Дата отсчета (строка 'YYYY-MM-DD'), если не указана — берется текущая
    :return: Словарь с тратами по месяцам
    """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    df = df[df["Категория"] == category]
    df["Месяц"] = df["Дата операции"].dt.to_period("M")
    report = df.groupby("Месяц")["Сумма операции"].sum().round(2).to_dict()
    report = {str(k): v for k, v in report.items()}
    return {"category": category, "spending": report}


@save_report_to_file
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца от переданной даты.
    :param transactions: DataFrame с транзакциями
    :param date: Дата отсчета (строка 'YYYY-MM-DD'), если не указана — берется текущая
    :return: Словарь с тратами по дням недели
    """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    df["weekday"] = df["Дата операции"].dt.day_name()
    report = df.groupby("weekday")["Сумма операции"].mean().round(2).to_dict()
    report = {str(k): v for k, v in report.items()}
    return {"spending_by_weekday": report}


@save_report_to_file
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Выводит средние траты в рабочий и выходной день за последние три месяца от переданной даты.
    :param transactions: DataFrame с транзакциями
    :param date: Дата отсчета (строка 'YYYY-MM-DD'), если не указана — берется текущая
    :return: Словарь с тратами по рабочим и выходным дням
    """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    df["is_workday"] = df["Дата операции"].dt.weekday < 5
    workday_mean = round(df[df["is_workday"]]["Сумма операции"].mean(), 2)
    weekend_mean = round(df[~df["is_workday"]]["Сумма операции"].mean(), 2)
    return {"workday_spending": workday_mean, "weekend_spending": weekend_mean}
