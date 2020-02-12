from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list':latest_question_list,
    }

    # 쿼리들의 질문을 나열한 것들을 합친 결과 : output
    # output=', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse("Hello, world. You're at the polls index!!")
    return render(request,'polls/index.html',context)

# 투표 상세 : 투표의 상세 항목 표시
def detail(request,question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #    question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    # return render(request,'polls/detail.html',{"question":question})
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

# 투표 결과 : 선택한 답변 반영 후 결과 보여줌
def results(request,question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

# 투표 기능 : 선택한 답변에 따라 +1해줌
def vote(request,question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',
                      {
                            'question':question,
                            'error_message':"아무것도 선택하지 않으셨습니다.",
                       }
                      )
    else:
        selected_choice.votes +=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
