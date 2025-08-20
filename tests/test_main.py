import pandas as pd
import sys
from src import main

def test_main(monkeypatch, tmp_path):
    # Создаём тестовый Excel-файл
    test_file = tmp_path / "operations.xlsx"
    df = pd.DataFrame({
        "Дата операции": ["01.01.2022 12:00:00"],
        "Категория": ["Супермаркеты"],
        "Сумма операции": [100]
    })
    df.to_excel(test_file, index=False)

    # Переопределяем функцию чтения, чтобы использовать тестовый файл
    monkeypatch.setattr(main, "read_excel_data", lambda path: pd.read_excel(test_file))

    # Перехватываем вывод
    from io import StringIO
    captured = StringIO()
    sys.stdout = captured
    main.main()
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "Столбцы файла" in output
    assert "Первые строки данных" in output
    assert "category" in output
