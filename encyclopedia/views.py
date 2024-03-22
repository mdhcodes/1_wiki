from django.shortcuts import render

# Imports required to redirect user to a diferent view.
from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Entry Page requirements must render page.html for each entry/page title (CSS, DJANGO, GIT, HTML, PYTHON, etc.) here.
def page(request, name):
    # name is the string typed after the port url (http://127.0.0.1:8000/) or the 'entry' value of the link clicked on the home page (index.html).  
    title = name
    # entry is a variable that stores a single entry/page retrieved by the function util.get_entry(title). Title may be any .md file stored in the entries folder (CSS, DJANGO, GIT, HTML, PYTHON, etc.).
    entry = util.get_entry(title)
    # If the entry does not exist...
    if entry is None:
        # Display none.html
        return render(request, "encyclopedia/none.html")
    else:
        # If the entry exists, display page.html with the following context ("dictionary of values to add to the template context").
        # render() - https://docs.djangoproject.com/en/5.0/topics/http/shortcuts/ 
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "entry": entry
        })


# Sidebar search functionality - when a query is typed in the search box, the program will attempt to find that entry/page title.
# If the search query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
# Implement a redirect to page
def search(request):
    # https://stackoverflow.com/questions/150505/how-to-get-get-request-values-in-django
    # Capture the value of q/query
    # !!! Entries are case sensitive at present. Must convert all data (title, entries, q) to upper- or lower-case. !!!
    title = request.GET.get("q", "")
    # entries is a variable that stores all entries/page titles in a list.
    entries = util.list_entries()
    # Test - print("Title", title)
    # Test - print("Entries", entries)
    # Test - print("Title in entries", title in entries)
    # If the title is in the list of entries...
    if title in entries:
        # Get the entry.
        entry = util.get_entry(title)
        # Redirect user to entry/title page results passing the GET request "q" value as kwargs. 
        # https://docs.djangoproject.com/en/5.0/ref/urlresolvers/
        return HttpResponseRedirect(reverse("page", kwargs={"name": title}))
    else:
        # If the title is not in the list of entries...
        # Display search.html.
        return render(request, "encyclopedia/search.html", {
            # If the query title does not match an entry, a search results page displays a list of all entries that have the query as a substring.
            # Clicking on any of the entry names on the search results page should take the user to that entry’s page.

        })