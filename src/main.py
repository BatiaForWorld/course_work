"""
Точка входа для запуска всех функциональностей приложения.
"""

import logging

from src.reports import spending_by_category
from src.utils import read_excel_data


def main():
    logging.basicConfig(level=logging.INFO)
    df = read_excel_data("data/operations.xlsx")
    print("Столбцы файла:", list(df.columns))
    print("Первые строки данных:")
    print(df.head())
    required_columns = {"Дата операции", "Категория", "Сумма операции"}
    if df.empty:
        print("Ошибка: файл данных пуст или не удалось загрузить данные.")
        return
    if not required_columns.issubset(df.columns):
        print(f"Ошибка: отсутствуют необходимые столбцы: {required_columns - set(df.columns)}")
        return
    date_time = "2021-12-12 12:12:12"
    result = spending_by_category(df, "Супермаркеты", date=date_time[:10])
    print(result)


if __name__ == "__main__":
    main()
