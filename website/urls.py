from django.urls import path
from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy', views.privacy, name='privacy'),
    path('login', views.login, name='login'),

]
