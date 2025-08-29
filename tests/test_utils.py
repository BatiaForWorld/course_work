import pandas as pd

from src.utils import get_period_dates, read_excel_data


def test_read_excel_data(tmp_path):
    # Создаём тестовый Excel-файл
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame(
        {"Дата операции": ["01.01.2022 12:00:00"], "Категория": ["Супермаркеты"], "Сумма операции": [100]}
    )
    df.to_excel(test_file, index=False)
    result = read_excel_data(str(test_file))
    assert not result.empty
    assert set(["Дата операции", "Категория", "Сумма операции"]).issubset(result.columns)

    # Проверка на несуществующий файл
    result = read_excel_data(str(tmp_path / "nofile.xlsx"))
    assert result.empty


def test_get_period_dates():
    # Месяц
    start, end = get_period_dates("2022-05-20", "M")
    assert start.day == 1
    assert end.day == 20
    # Неделя
    start, end = get_period_dates("2022-05-20", "W")
    assert start.weekday() == 0
    # Год
    start, end = get_period_dates("2022-05-20", "Y")
    assert start.month == 1 and start.day == 1
    # ALL
    start, end = get_period_dates("2022-05-20", "ALL")
    assert start.year == 1970
