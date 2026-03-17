const NORMALIZE_OPTS = { sensitivity: 'base' };

function normalize(text) {
    return (text || '').toLocaleLowerCase('pt-BR');
}

export function getArticles(root = document) {
    return Array.from(root.querySelectorAll('article.noticia')).map((element) => ({
        element,
        category: (element.dataset.category || '').toLocaleLowerCase('pt-BR'),
        title: element.querySelector('.Titulo_noticia')?.textContent?.trim() || '',
        summary: element.querySelector('.resumo')?.textContent?.trim() || '',
    }));
}

export function filterArticles(articles, query = '', category = 'all') {
    const q = normalize(query);
    const cat = normalize(category);

    return articles.filter((article) => {
        const matchesCategory = cat === 'all' || article.category === cat;
        const haystack = normalize(`${article.title} ${article.summary}`);
        const matchesQuery = !q || haystack.includes(q);
        return matchesCategory && matchesQuery;
    });
}

export function applyFilters({ root = document, query = '', category = 'all' } = {}) {
    const articles = getArticles(root);
    const filtered = filterArticles(articles, query, category);

    const visible = new Set(filtered.map((item) => item.element));
    articles.forEach((item) => {
        item.element.style.display = visible.has(item.element) ? '' : 'none';
    });

    return filtered.map((item) => item.title);
}

function setupSearch(root) {
    const form = root.querySelector('.search');
    const input = form?.querySelector('input[type="search"]');
    if (!form || !input) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
    });

    input.addEventListener('input', () => {
        const activeChip = root.querySelector('.chip.active');
        const category = activeChip?.dataset.category || 'all';
        applyFilters({ root, query: input.value, category });
    });
}

function setupChips(root) {
    const chips = Array.from(root.querySelectorAll('.chip'));
    chips.forEach((chip) => {
        chip.addEventListener('click', () => {
            chips.forEach((c) => c.classList.remove('active'));
            chip.classList.add('active');
            const input = root.querySelector('.search input[type=\"search\"]');
            const query = input?.value || '';
            applyFilters({ root, query, category: chip.dataset.category || 'all' });
        });
    });
}

function setupTicker(root) {
    const items = Array.from(root.querySelectorAll('.ticker-items span'));
    if (items.length <= 1) return;
    let current = 0;
    items[current].classList.add('visible');

    setInterval(() => {
        items[current].classList.remove('visible');
        current = (current + 1) % items.length;
        items[current].classList.add('visible');
    }, 4000);
}

function setupNewsletter(root) {
    const form = root.querySelector('.newsletter-form');
    const messageSlot = root.querySelector('.newsletter');
    if (!form) return;
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        form.reset();
        if (messageSlot) {
            messageSlot.dataset.state = 'submitted';
            messageSlot.querySelector('p')?.setAttribute('aria-live', 'polite');
        }
    });
}

export function initPortal(root = document) {
    applyFilters({ root, query: '', category: 'all' });
    setupSearch(root);
    setupChips(root);
    setupTicker(root);
    setupNewsletter(root);
}

if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => initPortal());
}
