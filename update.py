import requests
from datetime import datetime

def get_reddit_posts():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ClaudeDaily/1.0; +https://github.com)",
        "Accept": "application/json",
    }
    url = "https://www.reddit.com/r/ClaudeAI/hot.json?limit=8&raw_json=1"
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
    data = r.json()
    posts = data["data"]["children"]
    return [p["data"] for p in posts]

def generate_html(posts):
    fecha = datetime.now().strftime("%d %b %Y")
    items = ""
    for p in posts:
        titulo = p['title'].replace('<', '&lt;').replace('>', '&gt;')
        items += f"""
        <div class="post-card">
            <a href="https://reddit.com{p['permalink']}" target="_blank">
                <h3>{titulo}</h3>
            </a>
            <span>⬆ {p['score']} upvotes · r/ClaudeAI</span>
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

try:
    posts = get_reddit_posts()
    html = generate_html(posts)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html generado OK")
except Exception as e:
    print(f"Error: {e}")
    raise
