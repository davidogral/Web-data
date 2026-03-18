import os
from backend.scraper.scraper import (
    extract_titles,
    extract_categories,
    extract_links,
    extract_sources,
    extract_summaries,
    extract_dates,
)

# Pega o caminho absoluto para o index.html (agora na pasta frontend)
HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')

def read_html():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def test_extract_titles():
    """Deve extrair os títulos de todas as notícias"""
    html_content = read_html()
    titles = extract_titles(html_content)
    expected_titles = [
        "IA cresce no Brasil",
        "Python domina mercado",
        "Claude Code domina mercado",
        "Open-source LLMs ganham tração",
        "Investimentos em agentes autônomos sobem",
        "GPUs sob demanda encarecem",
        "Novo benchmark para code agents",
        "LLMs para saúde avançam",
        "Startups de agentes captam Série B",
        "Nova API de vetores chega ao mercado",
        "Brasil lança sandbox de IA",
        "Ferramentas open-source aceleram MLOps",
    ]
    assert titles == expected_titles

def test_extract_categories():
    """Deve extrair as categorias das notícias"""
    html_content = read_html()
    categories = extract_categories(html_content)
    expected_categories = [
        "Tecnologia",
        "Negócios",
        "Tecnologia",
        "Pesquisa",
        "Negócios",
        "Infra",
        "Pesquisa",
        "Saúde",
        "Negócios",
        "Infra",
        "Política",
        "Tecnologia",
    ]
    assert categories == expected_categories

def test_extract_links():
    """Deve extrair os links de 'Leia mais'"""
    html_content = read_html()
    links = extract_links(html_content)
    expected_links = [
        "noticia1.html",
        "noticia2.html",
        "noticia3.html",
        "noticia4.html",
        "noticia5.html",
        "noticia6.html",
        "noticia7.html",
        "noticia8.html",
        "noticia9.html",
        "noticia10.html",
        "noticia11.html",
        "noticia12.html",
    ]
    assert links == expected_links


def test_extract_sources():
    """Deve extrair as fontes de cada notícia"""
    html_content = read_html()
    sources = extract_sources(html_content)
    expected_sources = [
        "TechNews BR",
        "Dev Journal",
        "AI Daily",
        "AI Research Hub",
        "Venture AI",
        "Cloud Metrics",
        "BenchLab",
        "MedAI Times",
        "Venture AI",
        "Cloud Metrics",
        "GovTech BR",
        "OSS Radar",
    ]
    assert sources == expected_sources


def test_extract_summaries():
    """Deve extrair os resumos das notícias"""
    html_content = read_html()
    summaries = extract_summaries(html_content)
    expected_summaries = [
        "Avanços importantes e investimentos crescentes impulsionam o setor tecnológico nacional.",
        "Empresas adotam cada vez mais Python para soluções de análise de dados e machine learning.",
        "Adoção em alta de assistentes autônomos transforma a engenharia de software.",
        "Modelos abertos avançam em benchmarks e atraem contribuições corporativas.",
        "Rodadas de Series A focadas em agentes crescem 22% no trimestre.",
        "Preço-hora de instâncias com H100 sobe em média 18% na semana.",
        "Comunidade discute métricas mais realistas para avaliar agentes de código.",
        "Hospitais testam modelos especializados em protocolos clínicos com ganho de segurança.",
        "Rodadas acima de US$ 40M sinalizam maturidade do mercado de agentes autônomos.",
        "Provedores lançam camada gerenciada para indexação e busca semântica em larga escala.",
        "Ambiente regulatório controlado permitirá testes de IA com supervisão ética.",
        "Pipelines de IA ganham velocidade com novas libs de orquestração e observabilidade.",
    ]
    assert summaries == expected_summaries


def test_extract_dates():
    """Deve extrair as datas no formato ISO do atributo datetime"""
    html_content = read_html()
    dates = extract_dates(html_content)
    expected_dates = [
        "2026-03-17",
        "2026-03-16",
        "2026-03-15",
        "2026-03-14",
        "2026-03-13",
        "2026-03-12",
        "2026-03-11",
        "2026-03-17",
        "2026-03-17",
        "2026-03-14",
        "2026-03-16",
        "2026-03-15",
    ]
    assert dates == expected_dates
