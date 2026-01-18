from flask import Flask, render_template, send_from_directory
from blog import listarticles, renderarticle
import os

# check if there exist an articles folder, if not make one:
if os.path.exists("articles"):
    os.mkdir("articles")

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/articles")
def articles():
    availabe_articles = listarticles()
    return render_template("articles.html", articles=availabe_articles)

@app.route("/post/<filename>")
def post(filename: str):
    # 100% unsafe shit without proper sanitization, luckly I am an experienced
    # CTF player and I know what you silly fluff butts usually try to do, so here
    # are some sanitization (but if you do found any vulnerabilities in this website 
    # ill gladly put you in an upcoming hall of fame):
    safe_filename = filename.strip().replace("\n", "").replace("\r", "")
    safe_filename = os.path.normpath(safe_filename)

    html = renderarticle(f"articles/{safe_filename}.md")
    return render_template("post.html", content=html)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/rss")
def feed():
    return "WIP"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == "__main__":
    app.run("0.0.0.0", 8000)