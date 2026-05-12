import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
import hashlib

# ─── CONTENIDO FIJO: TIPS Y CASOS DE USO ─────────────────────────────────────

TIPS = [
    {
        "titulo": "Resumí cualquier PDF en 30 segundos",
        "categoria": "Productividad",
        "cuerpo": "Arrastrá un PDF al chat de Claude y escribí: 'Resumime este documento en 5 puntos clave para presentar al equipo'. Funciona con contratos, informes, papers, manuales. Ahorrás horas de lectura.",
        "emoji": "📄"
    },
    {
        "titulo": "Usá Claude para preparar reuniones difíciles",
        "categoria": "Trabajo",
        "cuerpo": "Antes de una reunión complicada, escribile a Claude: 'Voy a hablar con mi jefe sobre un aumento. Dame 5 argumentos sólidos basados en estos logros: [tus logros]'. Te da estructura y confianza.",
        "emoji": "💼"
    },
    {
        "titulo": "Analizá tu extracto bancario con IA",
        "categoria": "Finanzas",
        "cuerpo": "Copiá y pegá tus movimientos bancarios del mes y pedile: 'Categorizá estos gastos y decime en qué estoy gastando más. Dame 3 sugerencias para ahorrar'. Sin apps, sin registros, sin datos en servidores.",
        "emoji": "💳"
    },
    {
        "titulo": "Revisá contratos antes de firmar",
        "categoria": "Legal",
        "cuerpo": "Pegá el texto de cualquier contrato y escribí: 'Soy una persona sin conocimientos legales. ¿Qué cláusulas debería revisar con cuidado? ¿Hay algo inusual o riesgoso?' Claude te lo explica en lenguaje simple.",
        "emoji": "⚖️"
    },
    {
        "titulo": "Aprendé cualquier tema en 10 minutos",
        "categoria": "Aprendizaje",
        "cuerpo": "El prompt más poderoso para aprender: 'Explicame [tema] como si tuviese 15 años. Después dame 3 preguntas para autoevaluarme y los conceptos clave que debo recordar.'",
        "emoji": "🎓"
    },
    {
        "titulo": "Escribí emails difíciles sin estrés",
        "categoria": "Comunicación",
        "cuerpo": "¿Tenés que rechazar algo, pedir un favor importante o dar malas noticias? Describile la situación a Claude y pedile 3 versiones del email: formal, amigable y directa. Elegís la que más te representa.",
        "emoji": "✉️"
    },
    {
        "titulo": "Creá un plan de estudio personalizado",
        "categoria": "Aprendizaje",
        "cuerpo": "Escribí: 'Quiero aprender [tema] en [X semanas], tengo [X horas] por semana y ya sé [conocimiento previo]. Haceme un plan de estudio día por día con recursos gratuitos.' Claude lo arma como un tutor personal.",
        "emoji": "📚"
    },
    {
        "titulo": "El truco del ROL para mejores respuestas",
        "categoria": "Tips de Claude",
        "cuerpo": "El secreto para mejores respuestas: siempre incluí ROL + CONTEXTO + TAREA + FORMATO. Ejemplo: 'Actuá como nutricionista [ROL]. Soy adulto sin enfermedades [CONTEXTO]. Haceme un plan de comidas semanal [TAREA] en formato tabla [FORMATO].'",
        "emoji": "🎯"
    },
    {
        "titulo": "Traducí y adaptá contenido para Argentina",
        "categoria": "Contenido",
        "cuerpo": "No solo traducís: pedile 'Traducí este texto al español rioplatense, adaptá las referencias culturales para Argentina y usá un tono cercano para redes sociales'. La diferencia es enorme.",
        "emoji": "🌎"
    },
    {
        "titulo": "Usá Claude como sparring intelectual",
        "categoria": "Tips de Claude",
        "cuerpo": "En vez de pedirle que te dé la razón, escribí: 'Quiero defender la idea de [X]. Hacé de abogado del diablo y cuestioná mis argumentos más débiles'. Así mejorás tu pensamiento crítico.",
        "emoji": "🥊"
    },
    {
        "titulo": "Generá ideas de negocio en minutos",
        "categoria": "Emprendimiento",
        "cuerpo": "Prompt: 'Tengo [habilidad/experiencia] y quiero emprender con menos de [presupuesto]. Dame 5 ideas de negocio validadas con baja inversión inicial, explicando el modelo de ingresos de cada una.'",
        "emoji": "🚀"
    },
    {
        "titulo": "Analizá la competencia de tu negocio",
        "categoria": "Negocios",
        "cuerpo": "Describí tu negocio o idea y pedile: 'Hacé un análisis FODA de este negocio en el mercado argentino actual. ¿Cuál es el mayor riesgo y la mayor oportunidad?' Obtenés un análisis de consultor en segundos.",
        "emoji": "📊"
    },
    {
        "titulo": "Preparate para entrevistas de trabajo",
        "categoria": "Carrera",
        "cuerpo": "Pegá la descripción del puesto y tu CV y escribí: 'Simulá ser el entrevistador. Haceme las 10 preguntas más probables para este puesto y dame feedback de mis respuestas.' Practicás sin presión.",
        "emoji": "🤝"
    },
    {
        "titulo": "Mejorá cualquier texto manteniendo tu voz",
        "categoria": "Escritura",
        "cuerpo": "No uses Claude solo para corregir ortografía. Pedile: 'Reescribí este texto manteniendo mi voz pero haciéndolo más claro, conciso y persuasivo. Explicame los cambios principales que hiciste.'",
        "emoji": "✍️"
    },
]

CASOS_DE_USO = [
    {
        "titulo": "Cómo una contadora ahorra 3 horas por semana",
        "categoria": "Caso de uso real",
        "cuerpo": "Marcela, contadora en CABA, usa Claude para redactar emails a clientes explicando situaciones impositivas complejas en lenguaje simple. 'Antes me llevaba 40 minutos escribir cada email. Ahora le doy el contexto a Claude, reviso y mando en 5 minutos.'",
        "emoji": "💡"
    },
    {
        "titulo": "El estudiante que usa Claude como tutor 24/7",
        "categoria": "Caso de uso real",
        "cuerpo": "Tomás, estudiante de derecho, le pasa las sentencias que tiene que analizar y le pide que identifique los argumentos principales y los puntos débiles. 'Es como tener un profesor disponible a las 2 de la mañana antes del parcial.'",
        "emoji": "💡"
    },
    {
        "titulo": "Pyme que triplicó su presencia en redes",
        "categoria": "Caso de uso real",
        "cuerpo": "Una ferretería familiar de Rosario genera todo su contenido para Instagram con Claude. Le describe los productos de la semana y pide 5 posts con copy, hashtags y horario sugerido. Sin agencia, sin costo extra.",
        "emoji": "💡"
    },
    {
        "titulo": "Médico que usa Claude para comunicarse mejor",
        "categoria": "Caso de uso real",
        "cuerpo": "Un médico clínico le pasa las indicaciones técnicas que escribe en las recetas y Claude las reformula en lenguaje simple para que el paciente entienda exactamente qué tiene que hacer y por qué.",
        "emoji": "💡"
    },
]

ALL_CONTENT = TIPS + CASOS_DE_USO

def get_contenido_del_dia():
    dia = datetime.now().timetuple().tm_yday
    idx = dia % len(ALL_CONTENT)
    result = []
    for i in range(3):
        result.append(ALL_CONTENT[(idx + i) % len(ALL_CONTENT)])
    return result

# ─── NOTICIAS DE HACKER NEWS ─────────────────────────────────────────────────

KEYWORDS_IA = [
    "claude", "anthropic", "chatgpt", "openai", "gpt-4", "gpt-5",
    "llm", "gemini", "mistral", "llama", "deepseek",
    "artificial intelligence", " ai ", "machine learning",
    "deep learning", "neural network", "copilot", "cursor ai",
    "ai agent", "large language"
]

def get_hn_posts():
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        r = requests.get(url, timeout=15)
        ids = list(r.json())[:200]
        posts = []
        for id in ids:
            try:
                item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json", timeout=8).json()
                if item and isinstance(item, dict) and item.get("title"):
                    titulo = item["title"].lower()
                    if any(kw in titulo for kw in KEYWORDS_IA):
                        item["fuente"] = "Hacker News"
                        item["link_url"] = item.get('url', f"https://news.ycombinator.com/item?id={item['id']}")
                        posts.append(item)
                if len(posts) >= 8:
                    break
            except:
                continue
        return posts
    except:
        return []

# ─── NOTICIAS DE RSS ─────────────────────────────────────────────────────────

RSS_FEEDS = [
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
]

def get_rss_posts():
    posts = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; IADaily/1.0)"}
    for nombre, feed_url in RSS_FEEDS:
        try:
            r = requests.get(feed_url, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
            root = ET.fromstring(r.content)
            items = root.findall('.//item')
            for item in items[:4]:
                titulo_el = item.find('title')
                link_el = item.find('link')
                if titulo_el is not None and link_el is not None:
                    titulo = titulo_el.text or ''
                    link = link_el.text or ''
                    if titulo and link:
                        posts.append({
                            'title': titulo.strip(),
                            'link_url': link.strip(),
                            'fuente': nombre,
                            'score': 0,
                            'descendants': 0,
                            'id': hashlib.md5(link.encode()).hexdigest()[:8]
                        })
            if len(posts) >= 6:
                break
        except:
            continue
    return posts[:6]

# ─── GENERAR HTML ─────────────────────────────────────────────────────────────

def make_card_noticia(p, delay):
    titulo = p.get('title', '').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    url = p.get('link_url', '#')
    score = p.get('score', 0)
    comments = p.get('descendants', 0)
    fuente = p.get('fuente', 'Hacker News')
    meta = f'<span>&#11014; {score}</span><span>&#128172; {comments}</span>' if score > 0 else ''
    return f"""
    <article class="card card-noticia" data-cat="noticias" style="animation-delay:{delay:.2f}s">
        <div class="card-tag">&#128240; {fuente}</div>
        <a href="{url}" target="_blank" rel="noopener"><h2>{titulo}</h2></a>
        <div class="card-meta">{meta}<a class="src-link" href="{url}" target="_blank">Leer nota &#8599;</a></div>
    </article>"""

def make_card_contenido(c, delay):
    titulo = c['titulo'].replace('<', '&lt;').replace('>', '&gt;')
    cuerpo = c['cuerpo'].replace('<', '&lt;').replace('>', '&gt;')
    cat = c['categoria']
    emoji = c.get('emoji', '💡')
    return f"""
    <article class="card card-tip" data-cat="tips" style="animation-delay:{delay:.2f}s">
        <div class="card-tag">{emoji} {cat}</div>
        <h2>{titulo}</h2>
        <p class="card-body">{cuerpo}</p>
    </article>"""

def generate_html(noticias, contenido):
    fecha = datetime.now().strftime("%d %b %Y")
    cards_html = ""
    delay = 0
    if contenido:
        cards_html += make_card_contenido(contenido[0], delay)
        delay += 0.06
    for p in noticias:
        cards_html += make_card_noticia(p, delay)
        delay += 0.06
    for c in contenido[1:]:
        cards_html += make_card_contenido(c, delay)
        delay += 0.06
    if not cards_html:
        cards_html = '<p class="empty">Cargando contenido... Volvé en unos minutos.</p>'
    total = len(noticias) + len(contenido)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Daily - Noticias y tips de inteligencia artificial</title>
    <meta name="description" content="Las mejores noticias de IA, Claude y ChatGPT. Tips prácticos y casos de uso reales. Actualizado cada día.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,300&display=swap" rel="stylesheet">
    <style>
        :root {{
            --negro:#0f0f0f; --blanco:#f8f7f3; --acento:#c8310a;
            --acento2:#1a6b3c; --gris:#6a6a6a; --gris-claro:#e5e4df;
        }}
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Source Serif 4',Georgia,serif;background:var(--blanco);color:var(--negro);min-height:100vh;}}

        header{{border-bottom:3px solid var(--negro);padding:0 40px;position:sticky;top:0;background:var(--blanco);z-index:100;box-shadow:0 2px 8px rgba(0,0,0,0.06);}}
        .header-top{{display:flex;align-items:center;justify-content:space-between;padding:16px 0 12px;border-bottom:1px solid var(--gris-claro);}}
        .logo{{font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;letter-spacing:-1.5px;color:var(--negro);text-decoration:none;}}
        .logo em{{color:var(--acento);font-style:normal;}}
        .header-right{{display:flex;align-items:center;gap:16px;}}
        .badge{{background:var(--negro);color:var(--blanco);font-size:0.65rem;padding:4px 10px;letter-spacing:2px;text-transform:uppercase;}}
        .fecha-header{{font-size:0.75rem;color:var(--gris);text-transform:uppercase;letter-spacing:2px;}}

        .filtros-wrap{{display:flex;gap:6px;padding:10px 0;overflow-x:auto;scrollbar-width:none;}}
        .filtros-wrap::-webkit-scrollbar{{display:none;}}
        .filtro{{font-family:'Source Serif 4',serif;font-size:0.75rem;padding:5px 16px;border:1.5px solid var(--negro);background:transparent;cursor:pointer;white-space:nowrap;transition:all 0.15s;letter-spacing:0.5px;}}
        .filtro:hover,.filtro.active{{background:var(--negro);color:var(--blanco);}}

        .container{{max-width:780px;margin:0 auto;padding:36px 24px 80px;}}
        .seccion-label{{font-size:0.65rem;text-transform:uppercase;letter-spacing:4px;color:var(--gris);margin-bottom:20px;padding-bottom:8px;border-bottom:1px solid var(--gris-claro);}}

        .stat-bar{{display:flex;gap:32px;padding:20px 0;border-bottom:3px solid var(--negro);margin-bottom:28px;}}
        .stat-num{{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:900;color:var(--acento);line-height:1;}}
        .stat-label{{font-size:0.65rem;text-transform:uppercase;letter-spacing:2px;color:var(--gris);margin-top:4px;}}

        .card{{padding:22px 0;border-bottom:1px solid var(--gris-claro);animation:fadeUp 0.4s both;}}
        .card.oculta{{display:none;}}
        @keyframes fadeUp{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
        .card-tag{{font-size:0.65rem;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;}}
        .card-noticia .card-tag{{color:var(--acento);}}
        .card-tip .card-tag{{color:var(--acento2);}}
        .card h2{{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;line-height:1.35;margin-bottom:10px;}}
        .card-noticia a{{text-decoration:none;color:inherit;}}
        .card-noticia h2{{transition:color 0.15s;}}
        .card-noticia h2:hover{{color:var(--acento);}}
        .card-body{{font-size:0.92rem;line-height:1.7;color:#333;margin-top:6px;font-weight:300;}}
        .card-meta{{display:flex;align-items:center;gap:14px;font-size:0.75rem;color:var(--gris);margin-top:10px;}}
        .src-link{{color:var(--acento)!important;text-decoration:none;margin-left:auto;font-size:0.73rem;}}
        .src-link:hover{{text-decoration:underline;}}
        .empty{{color:var(--gris);font-style:italic;padding:40px 0;text-align:center;}}
        footer{{text-align:center;padding:28px;font-size:0.72rem;color:var(--gris);border-top:1px solid var(--gris-claro);letter-spacing:1px;}}

        @media(max-width:600px){{
            header{{padding:0 16px;}}
            .container{{padding:20px 16px 60px;}}
            .logo{{font-size:1.5rem;}}
            .card h2{{font-size:1.05rem;}}
            .stat-bar{{gap:16px;}}
            .stat-num{{font-size:1.6rem;}}
        }}
    </style>
</head>
<body>
<header>
    <div class="header-top">
        <a class="logo" href="#">IA<em>Daily</em></a>
        <div class="header-right">
            <span class="badge">Auto-actualizado</span>
            <span class="fecha-header">{fecha}</span>
        </div>
    </div>
    <div class="filtros-wrap">
        <button class="filtro active" data-cat="todos">&#127775; Todo</button>
        <button class="filtro" data-cat="noticias">&#128240; Noticias</button>
        <button class="filtro" data-cat="tips">&#128161; Tips & Casos de uso</button>
    </div>
</header>

<div class="container">
    <div class="stat-bar">
        <div class="stat"><div class="stat-num">{len(noticias)}</div><div class="stat-label">Noticias hoy</div></div>
        <div class="stat"><div class="stat-num">{len(contenido)}</div><div class="stat-label">Tips del día</div></div>
        <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Total</div></div>
    </div>
    <p class="seccion-label">Inteligencia artificial &mdash; {fecha}</p>
    <div id="grid">{cards_html}</div>
</div>

<footer>IADAILY &mdash; Se actualiza automáticamente cada día &mdash; Fuentes: Hacker News &middot; The Verge &middot; MIT Tech Review</footer>

<script>
    document.querySelectorAll('.filtro').forEach(btn => {{
        btn.addEventListener('click', () => {{
            document.querySelectorAll('.filtro').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cat = btn.dataset.cat;
            document.querySelectorAll('.card').forEach(card => {{
                card.classList.toggle('oculta', cat !== 'todos' && card.dataset.cat !== cat);
            }});
        }});
    }});
</script>
</body>
</html>"""

# ─── MAIN ─────────────────────────────────────────────────────────────────────

print("Obteniendo noticias de Hacker News...")
hn = get_hn_posts()
print(f"HN: {len(hn)} noticias")

print("Obteniendo noticias de RSS...")
rss = get_rss_posts()
print(f"RSS: {len(rss)} noticias")

noticias = hn + rss
contenido = get_contenido_del_dia()

print(f"Total noticias: {len(noticias)}")
print(f"Tips del dia: {len(contenido)}")

html = generate_html(noticias, contenido)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("OK - index.html generado correctamente")
