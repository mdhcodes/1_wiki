from django.shortcuts import render

# Imports required to redirect user to a diferent view.
from django.urls import reverse
from django.http import HttpResponseRedirect

# Import required to use Django Forms.
# https://docs.djangoproject.com/en/4.0/ref/forms/api/
from django import forms

# Import required to use random module.
# https://www.geeksforgeeks.org/random-numbers-in-python/
# https://www.w3schools.com/python/ref_random_choice.asp
import random

# Import to convert markdown to HTML.
import markdown2

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
        # Convert Markdown to HTML with markdown2
        # https://github.com/trentm/python-markdown2
        entry = markdown2.markdown(entry)
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
        return HttpResponseRedirect(reverse("page", kwargs={"name": entry}))
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
                # Send context to search.html
                # "entry": entry
                "entries": entries
            })
        

# New Page requirements must render new_page.html.
"""
Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    Users should be able to click a button to save their new page.
    When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
"""        

# Create a new form by creating a new class called CreatePageForm. This new class will collect the specified data from the user.
class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title") 
    # https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
    content = forms.CharField(widget=forms.Textarea(attrs={"name": "content"}))

def new_page(request):
    # POST request
    if request.method == "POST":
        # Store user data in a variable named form_data.
        form_data = CreatePageForm(request.POST)
        # If the form data is valid...
        if form_data.is_valid():
            # Capture all the data from the 'cleaned' version of the form_data within the class CreatePageForm(forms.Form) from the data field variables title and content.
            title = form_data.cleaned_data["title"]
            content = form_data.cleaned_data["content"]
            print("Form Title:", title)
            print("Form Content:", content)

            # If an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
            if util.entry_exists(title):
                error = "This title already exists."                    
                return render(request, "encyclopedia/new_page.html", {
                    "error": error,
                    "form": CreatePageForm() 
                })
            else:
                # Save the new page entry.
                util.save_entry(title, content)
                # Redirect user to the new entry’s page.
                return HttpResponseRedirect(reverse("page", kwargs={"name": title}))
    else:        
        # GET request
        return render(request, "encyclopedia/new_page.html", {
            # Send new form context to new_page.html.
            "form": CreatePageForm()        
        })
    

# Edit Page requirements must render edit.html
# Create a new form by creating a new class called EditPageForm. This new class will collect the specified data from the user.
class EditPageForm(forms.Form):
    title = forms.CharField(label="Title") 
    # https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
    textarea = forms.CharField(widget=forms.Textarea())

def edit(request, name):
    title = name
    # The variable existing_data will store a dictionary of the current entry page title and markdown/textarea key value pairs.
    # The dictionary is needed to initialize the Django form with this existing data.
    existing_data = util.get_initial_dict(title)
    # Populate textarea with existing markdown by specifying initial. 
    # https://www.geeksforgeeks.org/initial-form-data-django-forms/ 
    form = EditPageForm(initial = existing_data) 

    # POST request
    if request.method == "POST":
         # Store user data in a variable named form_data.
        form_revisions = EditPageForm(request.POST)
        # If the form revisions are valid...
        if form_revisions.is_valid():
            # Capture all the revisions from the 'cleaned' version of the form_revisions within the class EditPageForm(forms.Form) from the data field variables title and textarea.
            title = form_revisions.cleaned_data["title"]
            textarea = form_revisions.cleaned_data["textarea"]
            
            content = textarea
            print("Title:", title)
            print("Content:", content)
            # Save the entry's revisions.
            util.save_entry(title, content)
            # Redirect user to the revised entry page.
            return HttpResponseRedirect(reverse("page", kwargs={"name": title}))
        
        else:
            # Form is invalid
            error = "The form is invalid. Please check your changes."
            form = EditPageForm(initial = form_revisions)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    
    else:
        # GET request
        return render(request, "encyclopedia/edit.html", {
                "title": title,     
                "form": form           
            }) 
    

# Random Page requirements will direct user to a random page.html.
def random_page(request):
    # Get a random entry from the list of encyclopedia entries.
    entries = util.list_entries()
    random_entry = random.choice(entries)
    # Get the entry for the random entry specified.
    title = random_entry
    entry = util.get_entry(title)

    return render(request, "encyclopedia/page.html", {
            "title": title,
            "entry": entry        
    })