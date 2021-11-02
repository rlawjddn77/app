from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'app/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'app/detail.html', {'question':question, 'error_message':"어떤 것도 선택하지 않았습니다."})
    else:
        selected_choice.votes +=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('app:results', args=(question.id,)))