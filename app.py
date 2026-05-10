from flask import Flask, Response, request, render_template, send_from_directory
from werkzeug.exceptions import HTTPException
from blog import listarticles, renderarticle
import urllib.parse
import datetime
import rfeed
import os

# check if there exist an articles folder, if not make one:
if not os.path.exists("articles"): os.mkdir("articles")
if not os.path.exists("articles/files"): os.mkdir("articles/files")

# for private articles
if not os.path.exists("private"): os.mkdir("private")
if not os.path.exists("private/files"): os.mkdir("private/files")

def sanitize_filename(filename: str):
    safe_filename = filename.strip().replace("\n", "").replace("\r", "")
    safe_filename = os.path.normpath(f"/{safe_filename}")[1:]
    return safe_filename

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
    safe_filename = sanitize_filename(filename)

    with open(f"articles/{safe_filename}.md", "r") as f:
        title = f.readline().strip().replace("#", "")

    html = renderarticle(f"articles/{safe_filename}.md")
    return render_template("post.html", content=html, title=title, year=datetime.datetime.now().year)


@app.route("/articles/files/<filename>")
def files(filename: str):
    # This is used to send readers files, images, and other attachments
    # also do not worry about LFI or other vulns, here we use a safe
    # function from Flask
    safe_filename = sanitize_filename(filename)
    return send_from_directory("articles/files", safe_filename)


# for privately shared articles, only accessible trough links and will not be indexed
@app.route("/private/<filename>")
def privpost(filename: str):
    safe_filename = sanitize_filename(filename)

    with open(f"private/{safe_filename}.md", "r") as f:
        title = f.readline().strip().replace("#", "")

    html = renderarticle(f"private/{safe_filename}.md")
    return render_template("post.html", content=html, title=title, year=datetime.datetime.now().year)


@app.route("/private/files/<filename>")
def privfiles(filename: str):
    safe_filename = sanitize_filename(filename)
    return send_from_directory("private/files", safe_filename)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feed.xml")
def feed():
    articles = listarticles(-1)
    feeded_articles = []
    for post in articles:
        post: dict
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
        image="https://maxthecomputerfox.online/static/maxicon.png",
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

@app.errorhandler(Exception)
def page_not_found(e):
    if isinstance(e, HTTPException):
        return render_template('error.html', error=e), e.code
    return render_template("error.html", error="Something broke, max is on it"), 500

if __name__ == "__main__":
    app.run("0.0.0.0", 80)