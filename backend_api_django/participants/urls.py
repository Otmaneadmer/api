from django.urls import path 
from amphitheatres import views

# define the urls
urlpatterns = [
    path('participants/', views.amphitheatres),
    path('participants/<int:pk>/', views.amphitheatre_detail),
]