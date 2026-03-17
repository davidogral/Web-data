import sqlite3
from typing import List, Tuple

from backend.scraper.scraper import (
    extract_titles,
    extract_categories,
    extract_links,
    extract_sources,
    extract_summaries,
    extract_dates,
)


def _prepare_records(html_content: str) -> List[Tuple[str, str, str, str, str, str]]:
    titles = extract_titles(html_content)
    categories = extract_categories(html_content)
    links = extract_links(html_content)
    sources = extract_sources(html_content)
    summaries = extract_summaries(html_content)
    dates = extract_dates(html_content)

    # Garante alinhamento mesmo se listas divergirem
    total = min(len(titles), len(categories), len(links), len(sources), len(summaries), len(dates))
    records = []
    for i in range(total):
        records.append(
            (
                titles[i],
                categories[i],
                sources[i],
                links[i],
                summaries[i],
                dates[i],
            )
        )
    return records


def save_news_to_db(html_content: str, db_path: str = "news.db") -> int:
    """
    Cria (se não existir) a tabela news e insere registros extraídos do HTML.
    Retorna o número de linhas inseridas.
    """
    records = _prepare_records(html_content)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                source TEXT,
                link TEXT,
                summary TEXT,
                date TEXT
            )
            """
        )
        conn.executemany(
            "INSERT INTO news (title, category, source, link, summary, date) VALUES (?, ?, ?, ?, ?, ?)",
            records,
        )
        conn.commit()

    return len(records)
