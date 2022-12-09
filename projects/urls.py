from django.urls import path
from projects import views

urlpatterns = [
    path('train_code', views.train_code, name='train_code'),

]
