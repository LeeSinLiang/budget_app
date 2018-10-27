from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.project_list , name='list'),
    path('add/', views.ProjectCreateView.as_view() , name='create'),
    path('<slug>/', views.project_detail , name='detail'),
    path('<slug>/delete/', views.project_delete , name='delete'),
]