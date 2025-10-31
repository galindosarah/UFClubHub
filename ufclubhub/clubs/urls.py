from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('search/', views.search_clubs, name='search_clubs'),
path('test/', views.test_connection, name='test_connection'),
]