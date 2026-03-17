import logging
from bs4 import BeautifulSoup
from typing import Iterable, List, Union

SoupInput = Union[str, BeautifulSoup, None]
logger = logging.getLogger(__name__)


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
    missing_attr = 0
    for el in elements:
        if attr:
            value = el.get(attr)
            if value is None:
                missing_attr += 1
        else:
            value = el.text if hasattr(el, "text") else None
        if value:
            cleaned.append(value.strip())
    if missing_attr:
        logger.warning("Encontrados %s elementos sem atributo esperado '%s'.", missing_attr, attr)
    return cleaned


def _log_if_empty(items: List[str], label: str) -> None:
    """Emite warning quando a extração não encontrou itens (sinal de HTML fora do esperado)."""
    if not items:
        logger.warning("Nenhum item de '%s' foi encontrado no HTML fornecido.", label)


def extract_titles(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    items = _extract_text(soup.find_all('h2', class_='Titulo_noticia'))
    _log_if_empty(items, "títulos")
    return items


def extract_categories(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    items = _extract_text(soup.find_all('span', class_='categoria'))
    _log_if_empty(items, "categorias")
    return items


def extract_links(html_content: SoupInput) -> List[str]:
    soup = _ensure_soup(html_content)
    items = _extract_text(soup.select('.card-footer a'), attr='href')
    _log_if_empty(items, "links")
    return items


def extract_sources(html_content: SoupInput) -> List[str]:
    """Extrai as fontes das notícias (span.fonte)."""
    soup = _ensure_soup(html_content)
    items = _extract_text(soup.find_all('span', class_='fonte'))
    _log_if_empty(items, "fontes")
    return items


def extract_summaries(html_content: SoupInput) -> List[str]:
    """Extrai os resumos das notícias (parágrafos com classe resumo)."""
    soup = _ensure_soup(html_content)
    items = _extract_text(soup.find_all('p', class_='resumo'))
    _log_if_empty(items, "resumos")
    return items


def extract_dates(html_content: SoupInput) -> List[str]:
    """Extrai as datas no atributo datetime das tags <time>."""
    soup = _ensure_soup(html_content)
    items = _extract_text((t for t in soup.find_all('time') if t.has_attr('datetime')), attr='datetime')
    _log_if_empty(items, "datas")
    return items
