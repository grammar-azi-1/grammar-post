from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from account.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

# Create your views here.

def login(request):
    next = request.GET.get('next', reverse_lazy('home'))
    registerform = RegisterForm
    loginform = LoginForm

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save(False)
            return redirect(reverse_lazy('login'))
        
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if not user:
                pass
            else:
                dj_login(request, user)
                return redirect(next)

    context = {
        'registerform': registerform,
        'loginform': loginform
    }
    return render(request, 'login.html', context)

def logout(request):
    dj_logout(request)
    return redirect(reverse_lazy('login'))