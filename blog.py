from datetime import datetime
from pathlib import Path
import markdown
import warnings
import os

def listarticles(pagination=-1, page=1) -> list:
    files = os.listdir("articles/")
    files = sorted(files, reverse=True)

    # if the pagination is set to -1, that means the user wants all
    # available articles, else, set the page
    if pagination != -1:
        files = files[pagination*(page-1):pagination*(page)]
    
    working_articles = []

    for file in files:
        if file == "files": continue

        file_name = Path(file).stem # removes the .md part of the file

        # checks if the start of the file contains the date
        if len(file_name) < 8 or not file_name[:8].isdigit():
            warnings.warn(f"{file}: must start with yyyyMMdd", UserWarning)
            continue
        
        date_str = file_name[:8]

        try:
            date = datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            warnings.warn(f"Invalid date in filename: {date_str}", UserWarning)
            continue
        
        with open(f"articles/{file}", 'r') as f:
            title = f.readline().strip().replace("#", "")
        
        if not title:
            warnings.warn(f"{file} seesm to not have a title", UserWarning)
            continue

        working_articles.append({
            "title": title,
            "date": date.strftime("%Y/%m/%d"),
            "file": f"{file_name}"
        })
    
    return working_articles


def renderarticle(filepath) -> str:
    with open(filepath, "r") as f:
        articlemarkdown = f.read()
    html = markdown.markdown(articlemarkdown)
    return html



# print(listarticles())
# print(renderarticle("articles/20260101_article1.md"))