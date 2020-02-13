from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views import generic
from .models import Question, Choice

# Create your views here.
# 인덱스
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# 투표 상세 : 투표의 상세 항목 표시
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# 투표 결과 : 선택한 답변 반영 후 결과 보여줌
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# 투표 기능 : 선택한 답변에 따라 +1해줌
def vote(request,question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
                            'question':question,
                            'error_message':"아무것도 선택하지 않으셨습니다.",
                       })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
