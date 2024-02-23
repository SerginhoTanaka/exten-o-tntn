from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from user.models import Score
import json
import random
from django.templatetags.static import static

def index_game(request,user_id):
    path = '../../static/QA.json'
    
    user = get_object_or_404(User, pk=user_id)
    score = Score.objects.filter(user=user_id) #não está funcionando 
    
    
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
                    message = 'Parabéns, você acertou'
                    score.score += 10
                    score.save()
                else:
                    message = 'Errou! Estude mais, filisteu incircunciso'
                    score.score -= 5

                correct_answer = question['Alternativas'][question['Resposta']]
                actual_question = question['Pergunta']
                explanation = question['Explicacao']


            

    
        return render(request, "game/explanation.html", { 
                "question": actual_question,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "message": message,
                "user_id":user_id,
                "score ": score.score
            })
    
    with open(static(path=path), 'r') as qa:
        data = json.load(qa)

    question = data[random.choice(list(data.keys()))]
    return render(request, "game/index_game.html", {
        "question": question,
        "user_id":user_id
    })

