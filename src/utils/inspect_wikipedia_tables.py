import io
from pathlib import Path
import pandas as pd
import requests


def inspect(
    url: str,
    source_name: str,
    save_csv: bool = False,
) -> None:
    print("=" * 100)
    print(url)
    print("=" * 100)
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(io.StringIO(response.text))
    print(f"\nFound {len(tables)} table(s)\n")
    output_dir: Path | None = None
    if save_csv:
        output_dir = (
            Path(__file__).resolve().parents[2]
            / "temp"
            / "wikipedia"
            / source_name
        )
        output_dir.mkdir(parents=True, exist_ok=True)
    for index, df in enumerate(tables):
        print("-" * 100)
        print(f"TABLE {index}")
        print("-" * 100)
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")
        print("\nColumn names:")
        for column in df.columns:
            print(f"  - {column}")
        print("\nFirst rows:")
        print(df.head())
        print()
        if output_dir is not None:
            df.to_csv(
                output_dir / f"table_{index}.csv",
                index=False,
                encoding="utf-8-sig",
            )


if __name__ == "__main__":
    inspect(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        "sp500",
        save_csv=True,
    )
    inspect(
        "https://en.wikipedia.org/wiki/Nasdaq-100",
        "nasdaq100",
        save_csv=True,
    )
    inspect(
        "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
        "djia",
        save_csv=True,
    )
