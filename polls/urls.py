from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    #ex : /polls/
    #function view
    # path("", views.index, name="index"),
    #class view
    path("", views.IndexView.as_view(), name="index"),
    #ex : /polls/5/
    #function view
    # path("<int:question_id>/", views.detail , name="details"),
    #class view
    path("<int:pk>/", views.DetailView.as_view(), name="details"),
    #ex : /polls/5/results/
    #function view
    # path("<int:question_id>/results", views.results , name="results"),
    #class view
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"),
    #ex : /polls/5/vote/
    path("<int:question_id>/vote", views.vote , name="votes")
]
