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
# def lower_entries_remove():
#     # Call list_entries() loop over each and 
#     entries = list_entries()
#     print('Entries original list from util.py', entries)
#     for entry in entries:
#         entries.append(entry.lower())
#         print('After append', entries)
#         entries.remove(entry)
#         print('After remove', entries)
#         print('Entries list from util.py lower_entries()', entries)

#     return entries


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