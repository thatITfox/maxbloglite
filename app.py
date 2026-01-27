from flask import Flask, Response, request, render_template, send_from_directory
from blog import listarticles, renderarticle
import urllib.parse
import datetime
import rfeed
import os

# check if there exist an articles folder, if not make one:
if not os.path.exists("articles"):
    os.mkdir("articles")
if not os.path.exists("articles/files"):
    os.mkdir("articles/files")


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/articles")
def articles():
    user_page = request.args.get("page", "1")
    try:
        user_page = int(user_page)
    except:
        return render_template(
            "error.html", 
            error="sorry, but that's not a page number comrade"
        ), 500

    availabe_articles = listarticles(pagination=10, page=user_page)
    return render_template(
        "articles.html",
        articles=availabe_articles,
        current_page=user_page
    )

@app.route("/post/<filename>")
def post(filename: str):
    # 100% unsafe shit without proper sanitization, luckly I am an experienced
    # CTF player and I know what you silly fluff butts usually try to do, so here
    # are some sanitization (but if you do found any vulnerabilities in this website 
    # ill gladly put you in an upcoming hall of fame):
    safe_filename = filename.strip().replace("\n", "").replace("\r", "")
    safe_filename = os.path.normpath(safe_filename)

    with open(f"articles/{safe_filename}.md", "r") as f:
        title = f.readline().strip().replace("#", "")

    html = renderarticle(f"articles/{safe_filename}.md")
    return render_template("post.html", content=html, title=title, year=datetime.datetime.now().year)


@app.route("/files/<filename>")
def files(filename: str):
    # This is used to send readers files, images, and other attachments
    # also do not worry about LFI or other vulns, here we use a safe
    # function from Flask
    safe_filename = filename.strip().replace("\n", "").replace("\r", "")
    safe_filename = os.path.normpath(safe_filename)
    return send_from_directory("articles/files", filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feed.xml")
def feed():
    articles = listarticles(-1)
    feeded_articles = []
    for post in articles:
        post: dict
        print(post)
        print(urllib.parse.quote(post.get('file')))
        item_post = rfeed.Item(
            title=post.get("title"),
            link=f"https://maxthecomputerfox.online/post/{urllib.parse.quote(post.get('file'))}",
            author="Max",
            pubDate=datetime.datetime.strptime(post.get("date"), "%Y/%m/%d")
        )
        feeded_articles.append(item_post)
    
    feed = rfeed.Feed(
        title="Max The Computer Fox's small bloggin site",
        link="https://maxthecomputerfox.online/",
        description="Welcome to Max's blogging site, where I make and post my crazy ideas",
        language="en-US",
        items=feeded_articles
    )

    return Response(feed.rss(), mimetype="application/xml")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == "__main__":
    app.run("0.0.0.0", 80)