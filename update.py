import requests
from datetime import datetime

def get_posts():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url, timeout=15)
    print(f"Tipo: {type(r.json())}")
    print(f"Primeros datos: {str(r.json())[:100]}")
    ids = list(r.json())[:20]
    posts = []
    for id in ids:
        try:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
            item = requests.get(item_url, timeout=10).json()
            if item and isinstance(item, dict) and item.get("title"):
                posts.append(item)
            if len(posts) >= 8:
                break
        except:
            continue
    return posts

def generate_html(posts):
    fecha = datetime.now().strftime("%d %b %Y")
    items = ""
    for p in posts:
        titulo = p.get('title', '').replace('<', '&lt;').replace('>', '&gt;')
        url = p.get('url', f"https://news.ycombinator.com/item?id={p['id']}")
        score = p.get('score', 0)
        items += f"""
        <div class="post-card">
            <a href="{url}" target="_blank">
                <h3>{titulo}</h3>
            </a>
            <span>&#11014; {score} puntos · Hacker News</span>
        </div>
        """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Claude Daily</title>
    <style>
        body {{ font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
        h1 {{ font-size: 2.5rem; border-bottom: 3px solid black; padding-bottom: 10px; }}
        .fecha {{ color: #888; margin-bottom: 30px; }}
        .post-card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 15px; }}
        .post-card a {{ text-decoration: none; color: black; }}
        .post-card h3 {{ margin: 0 0 8px 0; }}
        .post-card span {{ color: #888; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <h1>Claude Daily</h1>
    <p class="fecha">Actualizado: {fecha}</p>
    {items}
</body>
</html>"""

posts = get_posts()
print(f"Posts encontrados: {len(posts)}")
html = generate_html(posts)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("OK")
