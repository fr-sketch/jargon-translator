# data_prep.py
import pandas as pd
from sklearn.model_selection import train_test_split
import csv

def create_splits(csv_path: str, train_path: str, valid_path: str, test_size: float = 0.2):
    df = pd.read_csv(
        csv_path,
        sep=";",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        encoding="utf-8"
    )

    # Переименуем столбцы под то, что ждёт модель
    df = df.rename(columns={
        "word": "source_text",
        "translate": "target_text"
    })

    train_df, valid_df = train_test_split(df, test_size=test_size, random_state=42)

    # Сохраняем уже в стандартном CSV с запятой (для datasets.load_dataset)
    train_df.to_csv(train_path, index=False)
    valid_df.to_csv(valid_path, index=False)

if __name__ == "__main__":
    create_splits("dataset.csv", "train.csv", "valid.csv")
