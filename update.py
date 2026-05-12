import requests
from datetime import datetime

CATEGORIAS = {
    "Claude & Anthropic": ["claude", "anthropic"],
    "ChatGPT & OpenAI": ["chatgpt", "openai", "gpt-4", "gpt-5", "gpt4", "gpt5"],
    "Modelos & LLMs": ["llm", "gemini", "mistral", "llama", "deepseek", "grok", "language model"],
    "IA General": ["artificial intelligence", " ai ", "machine learning", "deep learning", "neural network"],
    "Codigo & Dev": ["copilot", "cursor", "devin", "ai coding", "ai agent", "agentic"],
}

def clasificar(titulo):
    t = titulo.lower()
    for cat, keywords in CATEGORIAS.items():
        if any(kw in t for kw in keywords):
            return cat
    return "IA General"

def get_posts():
    all_keywords = [kw for kws in CATEGORIAS.values() for kw in kws]
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url, timeout=15)
    ids = list(r.json())[:200]
    posts = []
    for id in ids:
        try:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json", timeout=10).json()
            if item and isinstance(item, dict) and item.get("title"):
                titulo = item["title"].lower()
                if any(kw in titulo for kw in all_keywords):
                    item["categoria"] = clasificar(item["title"])
                    posts.append(item)
            if len(posts) >= 12:
                break
        except:
            continue
    return posts

def generate_html(posts):
    fecha = datetime.now().strftime("%d %b %Y")
    
    # Agrupar por categoria
    cats_usadas = list(dict.fromkeys([p["categoria"] for p in posts]))
    
    # Cards
    cards_html = ""
    for i, p in enumerate(posts):
        titulo = p.get('title', '').replace('<', '&lt;').replace('>', '&gt;')
        url = p.get('url', f"https://news.ycombinator.com/item?id={p['id']}")
        score = p.get('score', 0)
        comments = p.get('descendants', 0)
        cat = p.get('categoria', 'IA General')
        delay = i * 0.05
        
        cards_html += f"""
        <article class="card" data-cat="{cat}" style="animation-delay: {delay}s">
            <div class="card-tag">{cat}</div>
            <a href="{url}" target="_blank" rel="noopener">
                <h2>{titulo}</h2>
            </a>
            <div class="card-meta">
                <span>&#11014; {score}</span>
                <span>&#128172; {comments}</span>
                <a class="hn-link" href="https://news.ycombinator.com/item?id={p['id']}" target="_blank">Ver en HN</a>
            </div>
        </article>
        """

    # Filtros
    filtros_html = '<button class="filtro active" data-cat="todos">Todos</button>'
    for cat in cats_usadas:
        filtros_html += f'<button class="filtro" data-cat="{cat}">{cat}</button>'

    if not cards_html:
        cards_html = '<p class="empty">No hay noticias de IA hoy. Volve mañana.</p>'

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Daily — Noticias de inteligencia artificial</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
    <style>
        :root {{
            --negro: #0a0a0a;
            --blanco: #fafaf7;
            --acento: #d4380d;
            --gris: #6b6b6b;
            --gris-claro: #e8e8e4;
            --card-bg: #ffffff;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Source Serif 4', Georgia, serif;
            background: var(--blanco);
            color: var(--negro);
            min-height: 100vh;
        }}

        /* HEADER */
        header {{
            border-bottom: 3px solid var(--negro);
            padding: 0 40px;
            position: sticky;
            top: 0;
            background: var(--blanco);
            z-index: 100;
        }}

        .header-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 0 14px;
            border-bottom: 1px solid var(--gris-claro);
        }}

        .logo {{
            font-family: 'Playfair Display', serif;
            font-size: 1.9rem;
            font-weight: 900;
            letter-spacing: -1px;
            color: var(--negro);
            text-decoration: none;
        }}

        .logo span {{ color: var(--acento); }}

        .fecha-header {{
            font-size: 0.8rem;
            color: var(--gris);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        /* FILTROS */
        .filtros-wrap {{
            display: flex;
            gap: 4px;
            padding: 12px 0;
            overflow-x: auto;
            scrollbar-width: none;
        }}

        .filtros-wrap::-webkit-scrollbar {{ display: none; }}

        .filtro {{
            font-family: 'Source Serif 4', serif;
            font-size: 0.78rem;
            padding: 5px 14px;
            border: 1.5px solid var(--negro);
            background: transparent;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s;
            letter-spacing: 0.5px;
        }}

        .filtro:hover, .filtro.active {{
            background: var(--negro);
            color: var(--blanco);
        }}

        /* MAIN */
        main {{
            max-width: 860px;
            margin: 0 auto;
            padding: 40px 24px 80px;
        }}

        .seccion-titulo {{
            font-family: 'Playfair Display', serif;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: var(--gris);
            margin-bottom: 24px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--gris-claro);
        }}

        /* CARDS */
        .grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 0;
        }}

        .card {{
            padding: 24px 0;
            border-bottom: 1px solid var(--gris-claro);
            animation: fadeUp 0.4s both;
            transition: opacity 0.2s;
        }}

        .card.oculta {{
            display: none;
        }}

        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .card-tag {{
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--acento);
            font-weight: 400;
            margin-bottom: 8px;
        }}

        .card a {{
            text-decoration: none;
            color: inherit;
        }}

        .card h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: 12px;
            transition: color 0.15s;
        }}

        .card h2:hover {{ color: var(--acento); }}

        .card-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 0.78rem;
            color: var(--gris);
        }}

        .hn-link {{
            color: var(--acento) !important;
            font-size: 0.75rem;
            text-decoration: none;
            margin-left: auto;
        }}

        .hn-link:hover {{ text-decoration: underline; }}

        .empty {{
            color: var(--gris);
            font-style: italic;
            padding: 40px 0;
            text-align: center;
        }}

        /* FOOTER */
        footer {{
            text-align: center;
            padding: 30px;
            font-size: 0.75rem;
            color: var(--gris);
            border-top: 1px solid var(--gris-claro);
            letter-spacing: 1px;
        }}

        @media (max-width: 600px) {{
            header {{ padding: 0 16px; }}
            main {{ padding: 24px 16px 60px; }}
            .logo {{ font-size: 1.4rem; }}
            .card h2 {{ font-size: 1.05rem; }}
        }}
    </style>
</head>
<body>

<header>
    <div class="header-top">
        <a class="logo" href="#">IA<span>Daily</span></a>
        <span class="fecha-header">{fecha}</span>
    </div>
    <div class="filtros-wrap">
        {filtros_html}
    </div>
</header>

<main>
    <p class="seccion-titulo">Noticias destacadas de inteligencia artificial</p>
    <div class="grid" id="grid">
        {cards_html}
    </div>
</main>

<footer>
    IADAILY &mdash; Actualizado automáticamente cada día &mdash; Fuente: Hacker News
</footer>

<script>
    const filtros = document.querySelectorAll('.filtro');
    const cards = document.querySelectorAll('.card');

    filtros.forEach(btn => {{
        btn.addEventListener('click', () => {{
            filtros.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cat = btn.dataset.cat;
            cards.forEach(card => {{
                if (cat === 'todos' || card.dataset.cat === cat) {{
                    card.classList.remove('oculta');
                }} else {{
                    card.classList.add('oculta');
                }}
            }});
        }});
    }});
</script>

</body>
</html>"""

posts = get_posts()
print(f"Posts de IA encontrados: {{len(posts)}}")
html = generate_html(posts)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("OK - index.html generado")
