from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Entry Page requirements must include a url path to each entry/page title (CSS, DJANGO, GIT, HTML, PYTHON, etc.) here.
    path("<str:name>", views.page, name="page")
]
