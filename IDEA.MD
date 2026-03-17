Ideia do projeto:
Portal Inteligente de Notícias sobre Inteligência Artificial com Coleta Automatizada e Dashboard Analítico em Dash.

Conceito do projeto

O projeto consiste no desenvolvimento de um portal web de notícias focado em Inteligência Artificial, reunindo as notícias mais recentes e relevantes do setor, com links para as fontes originais.
Após a publicação do portal, será implementado um processo de coleta automatizada de dados da própria página, permitindo organizar, tratar e analisar essas informações em um dashboard interativo construído com Dash.

A proposta une três frentes importantes:

Desenvolvimento web front-end, com foco em layout moderno, responsivo e semântico

Coleta e tratamento de dados, a partir do conteúdo exibido no portal

Visualização analítica, transformando notícias em indicadores e gráficos úteis

Problema que o projeto resolve

Hoje, notícias sobre IA estão espalhadas em vários sites, blogs e portais. Isso dificulta acompanhar:

os temas mais discutidos

a frequência de publicações

as fontes mais ativas

as tendências do mercado de IA

O portal resolve isso ao centralizar notícias relevantes em um só lugar, enquanto o dashboard permite analisar padrões e tendências a partir dos dados coletados.

Objetivo geral

Desenvolver um portal de notícias sobre Inteligência Artificial, com interface moderna e responsiva, capaz de organizar conteúdos de forma clara e semântica, e integrar um processo de scraping para alimentar um dashboard analítico em Dash.

Objetivos específicos

Criar uma interface web moderna, limpa e responsiva

Estruturar o HTML de forma semântica e acessível

Exibir notícias com título, resumo, data, categoria, imagem e link da fonte original

Implementar um processo de scraping para coletar os dados exibidos na página

Armazenar e tratar os dados coletados

Construir um dashboard analítico com gráficos e filtros

Analisar tendências relacionadas ao universo da IA

Como o projeto pode funcionar
1. Portal de notícias

A página principal exibe cards com notícias sobre IA.
Cada notícia pode conter:

título

subtítulo ou resumo

data de publicação

fonte

categoria

imagem de destaque

botão para acessar a matéria original

Também pode haver:

barra de busca

filtro por categoria

seção de notícias em destaque

organização por data

página de detalhes da notícia

2. Coleta de dados

Depois que as notícias estiverem disponíveis no portal, um script faz o scraping da página para capturar informações como:

títulos

datas

categorias

links

quantidade de notícias por período

palavras mais frequentes

Esses dados podem ser salvos em:

CSV

SQLite 

3. Dashboard em Dash

Com os dados coletados, o dashboard pode mostrar:

quantidade de notícias por dia ou semana

categorias mais frequentes

fontes mais recorrentes

palavras-chave mais citadas

evolução temporal de temas de IA

distribuição por assunto

Diferencial acadêmico do projeto

O ponto forte da sua proposta é que ela não fica só no visual do portal. Ela mostra um fluxo completo:

coleta → organização → exibição → raspagem → análise

Isso torna o trabalho mais interessante porque envolve:

web design

HTML/CSS responsivo

scraping

tratamento de dados

visualização de informações

análise exploratória

Ou seja, é um projeto com cara de sistema completo, não apenas de site estático.

Estrutura sugerida do sistema
Módulo 1 — Front-end do portal

Tecnologias possíveis:

HTML5

CSS3

Responsabilidades:

montar a interface

garantir responsividade

organizar o conteúdo semanticamente

Módulo 2 — Coleta/Scraping

Tecnologias possíveis:

Python

Requests

BeautifulSoup

Responsabilidades:

acessar a página

extrair os dados das notícias

salvar em arquivo ou banco

Módulo 3 — Dashboard analítico

Tecnologias possíveis:

Python

Pandas

Plotly

Dash

Responsabilidades:

ler os dados coletados

tratar informações

gerar gráficos interativos

Sugestão de funcionalidades do portal
Essenciais

Página inicial com notícias em cards

Área de destaque para notícias principais

Links para fonte original

Layout responsivo

HTML semântico

Rodapé com informações do projeto

Intermediárias

Busca por palavra-chave

Filtro por categoria

Ordenação por data

Paginação ou carregamento progressivo

Avançadas

Sistema de recomendação por tema

Classificação automática por categorias

análise de sentimento dos títulos

feed atualizado automaticamente

Estrutura semântica recomendada do HTML

Para reforçar o requisito de HTML limpo e semântico, o portal pode usar:

header para topo e navegação

nav para menu principal

main para conteúdo principal

section para áreas como destaques e listagem

article para cada notícia

aside para filtros ou tendências

footer para informações finais

Isso valoriza muito a apresentação do projeto, porque mostra cuidado com boas práticas de desenvolvimento.

Ideia de identidade visual

Para um portal de IA, combina bem uma estética:

minimalista

moderna

com bastante contraste

uso de cards

espaçamento bem definido

fontes limpas

elementos visuais inspirados em tecnologia

Uma paleta interessante pode girar em torno de:

fundo claro ou escuro

azul, roxo ou ciano como cor de destaque

hover suave nos cards

sombras discretas

bordas arredondadas

Métricas interessantes para o dashboard

No Dash, você pode analisar coisas como:

total de notícias coletadas

número de notícias por categoria

top fontes publicadoras

frequência de termos como “LLM”, “OpenAI”, “robótica”, “automação”, “agentes”

evolução do número de notícias ao longo do tempo

ranking de temas mais recorrentes

Metodologia do projeto

Uma forma acadêmica de descrever a metodologia:

Levantamento de requisitos do portal

Definição da estrutura visual e semântica

Desenvolvimento do front-end

Implementação do script de coleta

Armazenamento e tratamento dos dados

Construção do dashboard analítico

Testes de responsividade e usabilidade

Avaliação dos resultados obtidos

Cuidados importantes para deixar o projeto mais maduro

Tem dois pontos que deixam a ideia mais profissional:

1. Fonte original sempre preservada

Como você quer mostrar notícias de outros lugares, o ideal é o portal funcionar como agregador, exibindo resumo e linkando para a fonte original, em vez de copiar conteúdo integral.

2. Scraping com responsabilidade

No texto do projeto, fica muito bom mencionar que a coleta de dados deve respeitar:

estrutura pública da página

limites éticos e técnicos

uso educacional

regras de acesso dos sites utilizados

Isso demonstra maturidade acadêmica.