from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """A página inicial de Learning Log"""
    return render(request, 'learning_logs/index.html')

def check_topic_owner(request, topic_id): # função de refatoração
    """Verifica se o usuário é o proprietário do tópico."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas"""

    # Garante que o assunto pertence ao usuário atual
    check_topic_owner(request, topic_id) #refatoração
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """adiciona um novo assunto."""
    if request.method != 'POST':
        #nenhum dado submetido; cria um formulario em branco
        form = TopicForm()
    else:
        #dados de POST submentidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Acrescenta uma nova entrada para um assunto em particular"""
    topic = Topic.objects.get(id=topic_id)
    topic_id = topic.id
    check_topic_owner(request, topic_id) #exatamente o mesmo que foi feito no def edit_entry, logo abaixo.
    if request.method != 'POST':
        #nenhum dado submetido; criar um formulario em branco
        form = EntryForm()
    else:
        #Dados de POST submetidos; processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    topic_id = topic.id # para padronização e melhor legibilidade
    """ topic_id = topic.id somente para padronizar e poder chamar topic_id no check_topic_owner de forma padronizado com o de cima, em def topic. Mas caso contrario, 
    seria necessario deixar topic.id, por motivo que ele é chamado em Diferença no fluxo de execução, no caso do def topic."""

    check_topic_owner(request, topic_id) #refatoração
    if request.method != 'POST':
        #Requisicao inicial; preenche previamente o formulario com  entrada atual
        form = EntryForm(instance=entry)
    else:
        #Dados de POST submetidos; processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
