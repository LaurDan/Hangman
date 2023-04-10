from django.urls import path
from api import views


urlpatterns = [
    path('rooms/', views.get_rooms),
    path('rooms/<str:pk>/', views.get_room)
]