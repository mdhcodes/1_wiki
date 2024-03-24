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
    # !!! Entries are case sensitive and data (title, entries, q) is converted to lower-case to compare. !!!
    title = request.GET.get("q", "") 
    # print("Title", title)
    # print("Entries", entries)
    # print("Title in entries", title in entries)
    
    # Convert entries to lowercase strings with util functions. 
    # Both functions work - util.lower_entries_range() and util.lower_entries(). Which function is faster???
    lowercase = util.lower_entries_range() # To search django was 3 requests - 54ms - Network Developer Tools
    # lowercase = util.lower_entries() # To search django was 3 requests - 59ms - Network Developer Tools
    # print('lowercase', lowercase)
    # print('title.lower()', title.lower())

    # If title.lower() is in the list of lowercase entries...
    if title.lower() in lowercase:
        # Get the entry.
        entry = util.get_entry(title)
        # Redirect user to entry/title page results passing the GET request "q" value as kwargs. 
        # https://docs.djangoproject.com/en/5.0/ref/urlresolvers/
        return HttpResponseRedirect(reverse("page", kwargs={"name": title.lower()}))
    else:
        # If the title is not in the list of entries...
        # If the query title does not match an entry, a search results page displays a list of all entries that have the query as a substring.
        
        # Title is the substring and title is accessed above.
        # Check title.lower() against all the entries.
        query_matches = util.find_substring_find(title.lower()) # Function uses find() - Speed according to Network Developer Tools - query 'hTM' - 54ms
        # query_match = util.find_substring_in(title.lower()) # Function uses in - Speed according to Network Developer Tools - query 'hTM' - 72ms 
        # Optimized for multiple matches.
        # If the entry.lower() is a substring of an element in lowercase...
        # if query_match[0]: # Only one match found
        # Multiple matches found.
        if len(query_matches) > 0:
            # Store the value in a variable. 
            # entry = query_match[0] #  Only one match found.
            # Store the values in a list.
            entries = query_matches
            # print("Title", title.lower())
            # print("Entry", entry)
            print('Query Matches Entries', entries)
            # Display the entry title that contains the substring on search.html.
            return render(request, "encyclopedia/search.html", {
                # Send context to search .html
                # "entry": entry
                "entries": entries
            })