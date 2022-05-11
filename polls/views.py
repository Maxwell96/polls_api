from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import JsonResponse
from .models import Poll

# This is a functional based view for implementing list view
def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {'results': list(polls.values('question', 'created_by', 'pub_date'))}
    return JsonResponse(data)

# This a functional based view for implementing detail view
def polls_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {'results':{
        'question': poll.question,
        'created_by': poll.created_by.username,
        'pub_date': poll.pub_date,
    }}
