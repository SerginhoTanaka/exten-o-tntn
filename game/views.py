from django.shortcuts import render

def index_game(request):
    return render(request, "game/index_game")