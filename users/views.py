from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def register(request):
    """Faz cadastro de um novo usuário."""
    if request.method == 'POST':
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Faz login do usuário
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            
            if authenticated_user:
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse('learning_logs:index'))
    else:
        # Exibe o formulário de cadastro em branco
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)
