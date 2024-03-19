from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Entry Page requirements must render page.html for each entry/page title (CSS, DJANGO, GIT, HTML, PYTHON, etc.) here.
def page(request, name):
    title = name
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/none.html")
    else:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "entry": entry
        })
