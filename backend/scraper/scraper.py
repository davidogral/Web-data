from bs4 import BeautifulSoup
from typing import Iterable, List, Union

SoupInput = Union[str, BeautifulSoup, None]


def _get_soup(html_content: str) -> BeautifulSoup:
    """Helper intern para evitar repetição da criação do BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')


def _ensure_soup(html_content: SoupInput) -> BeautifulSoup:
    """
    Aceita HTML em string ou um objeto BeautifulSoup já criado.
    Retorna uma instância de soup vazia quando a entrada for inválida.
    """
    if isinstance(html_content, BeautifulSoup):
        return html_content
    if isinstance(html_content, str):
        return _get_soup(html_content)
    # Entrada inválida/falsy → soup vazio para evitar exceptions
    return BeautifulSoup('', 'html.parser')


def _extract_text(elements: Iterable, attr: str = None) -> List[str]:
    """Extrai e limpa texto ou atributo quando existir, ignorando entradas vazias."""
    cleaned = []
    for el in elements:
        if attr:
            value = el.get(attr)
        else:
            value = el.text if hasattr(el, "text") else None
        if value:
            cleaned.append(value.strip())
    return cleaned


def extract_titles(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    return _extract_text(soup.find_all('h2', class_='Titulo_noticia'))


def extract_categories(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    return _extract_text(soup.find_all('span', class_='categoria'))


def extract_links(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    return _extract_text(soup.select('.card-footer a'), attr='href')


def extract_sources(html_content: SoupInput) -> List[str]:
    """Extrai as fontes das notícias (span.fonte)."""
    soup = _ensure_soup(html_content)
    return _extract_text(soup.find_all('span', class_='fonte'))


def extract_summaries(html_content: SoupInput) -> List[str]:
    """Extrai os resumos das notícias (parágrafos com classe resumo)."""
    soup = _ensure_soup(html_content)
    return _extract_text(soup.find_all('p', class_='resumo'))


def extract_dates(html_content: SoupInput) -> List[str]:
    """Extrai as datas no atributo datetime das tags <time>."""
    soup = _ensure_soup(html_content)
    return _extract_text((t for t in soup.find_all('time') if t.has_attr('datetime')), attr='datetime')
