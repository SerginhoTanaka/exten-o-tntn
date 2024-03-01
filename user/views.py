from django.shortcuts import render,redirect
from django.core.validators import validate_email,ValidationError
from user.models import User 


def index(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user is not None and user.password == password:
            user_id = user.id
            return redirect('index_game', user_id = user_id)
        else:
            return render(request, 'user/index.html', {'error': 'Usuário ou senha inválidos'})
        
    return render(request, 'user/index.html')

def signup(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password_confirmation')

        if not username or not password or not password2 or not email:
            return render(request, 'user/signup.html', {'error': 'Please fill all the fields'})
        
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'user/signup.html', {'error': 'Please enter a valid email'})

        if password != password2:
            return render(request, 'user/signup.html', {'error': 'Passwords do not match'})
        
        if len(password) < 6:
            return render(request, 'user/signup.html', {'error': 'Password must be at least 6 characters'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'user/signup.html', {'error': 'Username already taken'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'user/signup.html', {'error': 'Email already taken'})

        user = User(name=name,username=username, email=email, password=password)
        user.save()

        return redirect('index')
    
    return render(request, 'user/signup.html')

    
