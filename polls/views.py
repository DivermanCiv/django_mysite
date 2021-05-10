from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    """method to catch the 5 latest question ordered by publication date and return the
        index.html template in polls."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    """method to catch the casted vote on a question. If no choice has been selected, redirect
    to the polls/detail.html with an error message. Else, increment by 1 the vote count,
    save the vote and return a redirection to the polls/results page of the question"""

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes')+1
        # An F() object generate a SQL expression describing the required operation for the
        # database. It avoids concurrence conflicts (example : if 2 person tries to vote at the
        # same time, without F, the incrementation could be made only once instead of the
        # required 2 times)
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))