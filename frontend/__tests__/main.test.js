import { applyFilters, filterArticles, getArticles, initPortal } from '../main.js';

const html = `
    <section class="filters">
        <div class="filter-badges">
            <button type="button" class="chip active" data-category="all">Tudo</button>
            <button type="button" class="chip" data-category="tecnologia">Tecnologia</button>
            <button type="button" class="chip" data-category="negocios">Negócios</button>
        </div>
        <div class="search">
            <input type="search" />
            <button type="submit">Buscar</button>
        </div>
    </section>
    <section class="noticias">
        <article class="noticia card" data-category="tecnologia">
            <h2 class="Titulo_noticia">IA cresce no Brasil</h2>
            <p class="resumo">Avanços importantes impulsionam o setor.</p>
            <div class="card-footer"><time datetime="2026-03-17"></time><a href="noticia1.html">Leia mais</a></div>
        </article>
        <article class="noticia card" data-category="negocios">
            <h2 class="Titulo_noticia">Python domina mercado</h2>
            <p class="resumo">Empresas adotam cada vez mais Python.</p>
            <div class="card-footer"><time datetime="2026-03-16"></time><a href="noticia2.html">Leia mais</a></div>
        </article>
        <article class="noticia card" data-category="tecnologia">
            <h2 class="Titulo_noticia">Claude Code domina mercado</h2>
            <p class="resumo">Assistentes autônomos em alta.</p>
            <div class="card-footer"><time datetime="2026-03-15"></time><a href="noticia3.html">Leia mais</a></div>
        </article>
    </section>
`;

const resetDOM = () => {
    document.body.innerHTML = html;
};

describe('Portal front-end interactions', () => {
    beforeEach(() => {
        resetDOM();
    });

    test('filterArticles respeita categoria escolhida', () => {
        const articles = getArticles();
        const result = filterArticles(articles, '', 'negocios');
        expect(result).toHaveLength(1);
        expect(result[0].title).toContain('Python');
    });

    test('applyFilters combina busca e categoria', () => {
        applyFilters({ root: document, query: 'Claude', category: 'all' });
        const visible = Array.from(document.querySelectorAll('article')).filter(
            (el) => el.style.display !== 'none'
        );
        expect(visible).toHaveLength(1);
        expect(visible[0].dataset.category).toBe('tecnologia');
    });

    test('initPortal liga chips para filtrar notícias', () => {
        initPortal();
        const chipNegocios = document.querySelector('.chip[data-category="negocios"]');
        chipNegocios.click();
        const visibles = Array.from(document.querySelectorAll('article')).filter(
            (el) => el.style.display !== 'none'
        );
        expect(visibles).toHaveLength(1);
        expect(visibles[0].dataset.category).toBe('negocios');
    });
});
