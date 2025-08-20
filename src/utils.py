"""
Вспомогательные функции для работы с данными и датами.
"""

import logging
from datetime import datetime

import pandas as pd


def read_excel_data(filepath: str) -> pd.DataFrame:
    """
    Чтение данных из Excel-файла.
    :param filepath: Путь к файлу
    :return: DataFrame с транзакциями
    """
    try:
        df = pd.read_excel(filepath)
        logging.info(f"Данные успешно загружены из {filepath}")
        return df
    except Exception as e:
        logging.error(f"Ошибка при чтении Excel: {e}")
        return pd.DataFrame()


def get_period_dates(date_str: str, period: str = "M") -> tuple:
    """
    Получение диапазона дат по периоду (месяц/неделя/год/все).
    :param date_str: Дата в формате 'YYYY-MM-DD'
    :param period: 'M', 'W', 'Y', 'ALL'
    :return: (start_date, end_date)
    """
    end_date = datetime.strptime(date_str, "%Y-%m-%d")
    if period == "M":
        start_date = end_date.replace(day=1)
    elif period == "W":
        start_date = end_date - pd.Timedelta(days=end_date.weekday())
    elif period == "Y":
        start_date = end_date.replace(month=1, day=1)
    elif period == "ALL":
        start_date = datetime(1970, 1, 1)
    else:
        start_date = end_date.replace(day=1)
    return start_date, end_date
