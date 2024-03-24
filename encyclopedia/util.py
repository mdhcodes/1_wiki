import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


# Function to convert entries to lowercase strings.
# Using entries.append() and entries.remove() mutated the entries list and altered the element positions and indexing which caused the loop to skip elements.
"""
def lower_entries_remove():
    # Call list_entries() loop over each and 
    entries = list_entries()
    print('Entries original list from util.py', entries)
    for entry in entries:
        entries.append(entry.lower())
        print('After append', entries)
        entries.remove(entry)
        print('After remove', entries)
        print('Entries list from util.py lower_entries()', entries)

    return entries
"""


# Function to convert entries to lowercase strings.
# Eliminates altering element positions and indexing. Works.
def lower_entries_range():
    entries = list_entries()
    for i in range(len(entries)):
        # print('Entry', entries[i])
        new_entry = entries[i].lower()
        # print('Before assignment', entries)
        entries[i] = new_entry
        # print('After assignment', entries)

    return entries


# Function to convert entries to lowercase strings.
# Alternate solution for converting entries to lowercase. 
def lower_entries():
    entries = list_entries()
    for entry in entries:
        # print('Entry', entry)
        entries[entries.index(entry)] = entry.lower()
        # print('After assignment', entries)

    return entries


# Function that checks to see if user input is a substring of an entry.
# query is the substring.
def find_substring_find(query):
    # The match variable stores the list that will capture the entry value(s) that match the query/substring.
    matches = []
    # Create a list of all the entries.
    entries = list_entries()
    # Loop over the list of entries to find any that match an entry.
    for entry in entries:
        # find() returns the first index where the substring is found. Since the string might begin at the first index(0), the results of find must be > or == to 0.   
        # https://www.freecodecamp.org/news/python-find-how-to-search-for-a-substring-in-a-string/
        if entry.lower().find(query) >= 0:
        # Store the entry matches in the list named match.
            matches.append(entry)
            
    return matches


# Find substring using 'in'
def find_substring_in(query):
    matches = []
    entries = lower_entries_range()
    print('Entries', entries)
    print('query', query)
    for entry in entries:
        print('Entry', entry)
        if query.lower() in entry:
            matches.append(entry)

    return matches


# Function checks if an encyclopedia title/entry already exists. 
def entry_exists(title):
    check = []
    entries = lower_entries_range()
    for entry in entries:
        if title.lower() == entry:
            check.append(entry)

    if len(check) > 0:
        return True
    else:
        return False
