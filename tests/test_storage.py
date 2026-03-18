import os
import sqlite3

from backend.scraper.storage import save_news_to_db

HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')


def read_html():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def test_save_news_to_db_creates_table_and_inserts_rows(tmp_path):
    html_content = read_html()
    db_path = tmp_path / "news.db"

    inserted = save_news_to_db(html_content, db_path=str(db_path))

    assert inserted == 12
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT title, category, source, link, summary, date FROM news ORDER BY id"
    ).fetchall()
    conn.close()

    assert rows == [
        ("IA cresce no Brasil", "Tecnologia", "TechNews BR", "noticia1.html", "Avanços importantes e investimentos crescentes impulsionam o setor tecnológico nacional.", "2026-03-17"),
        ("Python domina mercado", "Negócios", "Dev Journal", "noticia2.html", "Empresas adotam cada vez mais Python para soluções de análise de dados e machine learning.", "2026-03-16"),
        ("Claude Code domina mercado", "Tecnologia", "AI Daily", "noticia3.html", "Adoção em alta de assistentes autônomos transforma a engenharia de software.", "2026-03-15"),
        ("Open-source LLMs ganham tração", "Pesquisa", "AI Research Hub", "noticia4.html", "Modelos abertos avançam em benchmarks e atraem contribuições corporativas.", "2026-03-14"),
        ("Investimentos em agentes autônomos sobem", "Negócios", "Venture AI", "noticia5.html", "Rodadas de Series A focadas em agentes crescem 22% no trimestre.", "2026-03-13"),
        ("GPUs sob demanda encarecem", "Infra", "Cloud Metrics", "noticia6.html", "Preço-hora de instâncias com H100 sobe em média 18% na semana.", "2026-03-12"),
        ("Novo benchmark para code agents", "Pesquisa", "BenchLab", "noticia7.html", "Comunidade discute métricas mais realistas para avaliar agentes de código.", "2026-03-11"),
        ("LLMs para saúde avançam", "Saúde", "MedAI Times", "noticia8.html", "Hospitais testam modelos especializados em protocolos clínicos com ganho de segurança.", "2026-03-17"),
        ("Startups de agentes captam Série B", "Negócios", "Venture AI", "noticia9.html", "Rodadas acima de US$ 40M sinalizam maturidade do mercado de agentes autônomos.", "2026-03-17"),
        ("Nova API de vetores chega ao mercado", "Infra", "Cloud Metrics", "noticia10.html", "Provedores lançam camada gerenciada para indexação e busca semântica em larga escala.", "2026-03-14"),
        ("Brasil lança sandbox de IA", "Política", "GovTech BR", "noticia11.html", "Ambiente regulatório controlado permitirá testes de IA com supervisão ética.", "2026-03-16"),
        ("Ferramentas open-source aceleram MLOps", "Tecnologia", "OSS Radar", "noticia12.html", "Pipelines de IA ganham velocidade com novas libs de orquestração e observabilidade.", "2026-03-15"),
    ]
