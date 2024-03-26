from django.urls import path

from . import views

# Order matters for urlpatterns. 
# https://docs.djangoproject.com/en/5.0/topics/http/urls/
# How Django processes a request: 
# 3. Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL, matching against path_info.
# As a result, path("<str:name>", views.page, name="page") must be last since it is not specific and takes any string.
urlpatterns = [
    path("", views.index, name="index"),
    # Search Page requirements must include a url path to search.html here.
    path("search", views.search, name="search"),
    # New Page requirements must include a url path to new_page.html here.
    path("new_page", views.new_page, name="new_page"),
    # Edit Page requirements must include a url path to edit.html here.
    path("edit/<str:name>", views.edit, name="edit"),
    # Entry Page requirements must include a url path to each entry/page title (CSS, DJANGO, GIT, HTML, PYTHON, etc.) here.
    path("<str:name>", views.page, name="page")
]
