from django.shortcuts import render

from user.models import User
import json
import random
from django.templatetags.static import static


def index_game(request, user_id):

    path = '../../static/QA.json'

    user = User.objects.get(pk=user_id)
    
    if request.method == "POST":
                
        user_answer = request.POST.get('resposta')
        question_data = request.POST.get('pergunta')

        with open(static(path=path), 'r') as qa:
            data = json.load(qa)

        correct_answer = ''
        message = ''
        explanation = ''
        for question in data.values():
            if question['Pergunta'] == question_data:
                if question['Resposta'] == user_answer:
                    message = 'Parabéns, você acertou!'
                    user.score += 10
                    user.save()
                else:
                    message = 'Errou! Estude mais, filisteu incircunciso'
                    user.score -= 5
                    user.save()

                correct_answer = question['Alternativas'][question['Resposta']]
                actual_question = question['Pergunta']
                explanation = question['Explicacao']

        data = {
            "question": actual_question,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "message": message,
            "user_id": user_id,
            "score": user.score
        }
        return render(request, "game/explanation.html", data)
    
    with open(static(path=path), 'r') as qa:
        data = json.load(qa)

    question = data[random.choice(list(data.keys()))]
    return render(request, "game/index_game.html", {
        "question": question,
        "user_id": user_id
    })


def leaderboard(request, user_id):

    users = User.objects.all().order_by('-score')[:10]

    return render(request, "game/leaderboard.html", {
        "users": users,
        "user_id": user_id
        })

