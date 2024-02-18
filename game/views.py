from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import json
import random

def index_game(request, user_id):
    
    with open('../static/QA.json', 'r') as qa:
        data = json.load(qa)

    question = data[random.choice(list(data.keys()))]
    correct_answer = question['Resposta']
    explanation = question['Explicacao']

    user = get_object_or_404(User, pk=user_id)
    # score = Score.objects.get(user=User)
    
    if request.method == "POST":
        user_answer = request.POST.getlist('resposta')

        if(user_answer != None):
            
            if(user_answer == correct_answer):
                # score.score += 1
                # score.save()
                return render(request, "game/index_game", { 
                        "question": question,
                        "correct_answer": correct_answer,
                        "explanation": explanation,
                        "score": score.score
                    })
            
            
        
    return render(request, "game/index_game", { 
            "question": question,
            "score": score.score
        })
