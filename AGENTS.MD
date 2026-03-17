# BPKnews - Portal de Inteligência Artificial: Guia do Agente e Documentação

Este documento centraliza a arquitetura, regras de negócio, padrões de código e histórico de problemas do projeto BPKnews. Ele deve ser atualizado continuamente à medida que o projeto evolui.

## 1. Visão Geral da Arquitetura e Stack Tecnológico

O portal BPKnews é um agregador de notícias de Inteligência Artificial composto por três módulos principais: Front-end, Coleta de Dados (Scraping) e Dashboard Analítico.

**Stack Tecnológico:**
- **Front-end:** HTML5 semântico, CSS3 (Vanilla).
- **Processamento de Dados e Scraping:** Python 3.9+, BeautifulSoup4, Requests, Pytest (para TDD).
- **Dashboard / Análise (Futuro):** Pandas, Plotly, Dash.

**Módulos / Serviços Atuais:**
- `frontend/index.html` / `frontend/style.css`: Interface do portal exibindo os cards de notícias.
- `backend/scraper/scraper.py`: Serviço de extração de dados do HTML local (e futuramente da web) utilizando BeautifulSoup.
- `tests/test_scraper.py`: Testes unitários das funções de scraping (seguir ciclo TDD).

## 2. Estrutura de Diretórios e Variáveis

**Estrutura Atual:**
```
Web+data/
├── frontend/
│   ├── index.html        # Página principal do portal
│   └── style.css         # Estilos da página
├── backend/
│   └── scraper/
│       └── scraper.py    # Script principal de extração de dados
├── tests/
│   └── test_scraper.py   # Testes unitários do scraper (Pytest)
├── requirements.txt      # Dependências do projeto Python
├── IDEA.MD               # Documentação original do escopo
├── README.md             # Resumo do repositório
└── AGENTS.MD             # Este documento (Guia do projeto)
```

**Variáveis de Ambiente:**
*(Nenhuma variável de ambiente necessária no momento. Serão adicionadas quando implementarmos DB e deploy).*

## 3. Regras, Convenções e Design Patterns

- **Metodologia TDD (Test-Driven Development):** Todo novo desenvolvimento (especialmente do módulo em Python) **DEVE** seguir estritamente o ciclo TDD:
  1. **RED:** Criar testes unitários primeiro garantindo que eles falhem.
  2. **GREEN:** Implementar a funcionalidade mínima necessária para fazer os testes passarem.
  3. **REFACTOR:** Refatorar o código para melhorar estrutura, legibilidade e performance sem quebrar os testes.
- **Scraping Helper:** Para módulos de extração (ex: `scraper.py`), não instanciar o `BeautifulSoup` em cada função independentemente. Usar uma função auxiliadora (wrapper `_get_soup`) ou passar o objeto soup já instanciado para otimizar performance.
- **Entrada flexível e validação:** Funções de extração devem aceitar HTML em `str` ou um objeto `BeautifulSoup` já criado, retornando listas vazias quando a entrada for inválida ou campos estiverem ausentes, evitando exceções.
- **HTML Semântico:** Modificações na UI devem respeitar tags semânticas ( `<header>`, `<main>`, `<section>`, `<article>`, `<footer>`).
- **Nomenclatura de Classes CSS:** Padrões claros focados no componente (ex: `.card`, `.card-content`, `.card-meta`).

## 4. Histórico de Problemas (Common Hurdles)

- **Problema:** Repetição de processamento de HTML em múltiplas funções de extração (Scraper).
  - **Solução:** Implementado helper `_get_soup` no `scraper.py` durante a fase de REFACTOR do TDD para evitar instanciar `BeautifulSoup` repetidamente para o mesmo conteúdo HTML. Isso melhora a performance e limpa o código. *[Resolvido em 17 Mar 2026]*
- **Problema:** Garantir a asserção correta no TDD (fase RED).
  - **Solução:** Os testes iniciais precisam ter os expects corretos e o código de origem precisa retornar um valor diferente (ex: `None` ou `pass`) em vez de código funcional, validando assim que o teste realmente testa o que deve no ambiente do Pytest. *[Resolvido em 17 Mar 2026]*
- **Problema:** Falta de robustez ao lidar com HTML parcial/None causava exceções ou resultados inconsistentes.
  - **Solução:** Criados helpers `_ensure_soup` e `_extract_text` para validar entrada, normalizar texto/atributos e retornar listas vazias quando apropriado; todas as funções de extração (títulos, categorias, links, fontes, resumos, datas) utilizam esses helpers. *[Resolvido em 17 Mar 2026]*

## 5. Processos Operacionais

*(Será populado quando as rotinas de scraper recorrentes ou jobs em background forem implementados)*

> **Nota para o Agente:** Este arquivo é vivo. Sempre que resolver um bug complexo, estender a arquitetura, ou definir um novo padrão de projeto (ex: padrão de conexão com banco de dados no futuro), atualize a seção correspondente neste arquivo.
