from django.urls import path
from knowledges import views

urlpatterns = [
    path('knowledge_list', views.knowledge_list, name='knowledge_list'),
    path('knowledge_delete', views.knowledge_delete, name='knowledge_delete'),

]
