
from django.urls import path
from .views import home_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('today-in-space/', views.today_in_space, name='today_in_space'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('isro-tweet/', views.isro_tweet, name='isro_tweet'),
]