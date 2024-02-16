from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.core.validators import validate_email,ValidationError
from django.contrib.auth.models import User 


# Create your views here.
def index(request):

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('index')
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

        user = User.objects.create_user(first_name=name,username=username, email=email, password=password)
        user.save()

        return redirect('index')
    
    return render(request, 'user/signup.html')

    
