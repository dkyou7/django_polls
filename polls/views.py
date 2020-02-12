from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

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
    return HttpResponse("You're looking at question %s." % question_id)

# 투표 결과 : 선택한 답변 반영 후 결과 보여줌
def results(request,question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# 투표 기능 : 선택한 답변에 따라 +1해줌
def vote(request,question_id):
    return HttpResponse("You're voting on question %s." % question_id)