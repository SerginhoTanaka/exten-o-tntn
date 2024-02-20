from django.urls import path
from . import views
urlpatterns = [
    path('index_game/<int:user_id>/', views.index_game, name="index_game")
]
