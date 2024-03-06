from django.shortcuts import render, redirect
from user.models import User
import json
import random
from django.templatetags.static import static


def index_game(request, user_id, question_id=None):

    if request.method == "POST":

        user_answer = request.POST.get('resposta')
        path = '../../static/QA.json'
        user = User.objects.get(pk=user_id)
        
        with open(static(path=path), 'r') as qa:
            data = json.load(qa)

        question = data[str(question_id)]

        if question['Resposta'] == user_answer:
            message = 'Parabéns, você acertou!'
            user.score += 10
            user.save()
        else:
            message = 'Infelizmente a resposta está incorreta'
            user.score -= 5
            user.save()

        data = {
            "question": question['Pergunta'],
            "correct_answer": question['Alternativas'][question['Resposta']],
            "explanation": question['Explicacao'],
            "message": message,
            "user_id": user_id,
            "score": user.score,
        }

        return render(request, "game/explanation.html", data)

    path = '../../static/QA.json'
    
    with open(static(path=path), 'r') as qa:
        data = json.load(qa)

    question_id = int(random.choice(list(data.keys())))
    question = data[str(question_id)]
    data = {
        "question": question,
        "user_id": user_id,
        "question_id": question_id
    }

    return render(request, "game/index_game.html", data)

def leaderboard(request, user_id):

    users = User.objects.all().order_by('-score')[:10]

    return render(request, "game/leaderboard.html", {
        "users": users,
        "user_id": user_id
        })
