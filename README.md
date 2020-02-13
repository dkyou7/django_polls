- #### init script

  ```bash
  pip install django	# 가상환경에서 장고 설치
  django-admin startproject config .	# config 파일 설치
  python manage.py startapp polls	# 만들고자 하는 앱 생성! cmd
  ```

- #### 뷰 만들기 - views.py

  - Controller 의 역할 수행한다.

  - 간단한 코드를 입력해보자.

    ```python
    from django.http import HttpResponse
    
    # Create your views here.
    def index(request):
        return HttpResponse("Hello, world index!!")
    ```

  - 뷰를 만들면 이 뷰를 호출하기 위한 URL이 있어야 한다.

- #### polls/urls.py

  ```python
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('',views.index,name='index'),	
      # '' : 주소를 의미
  	# views.index : 주소로 접근 시 호출할 뷰.
  	# name='index' : 원하는 곳에서 이 이름을 가지고 주소를 호출해 출력
  ]
  ```

- #### config/urls.py

  ```python
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('polls/',include('polls.urls'))
      # polls/urls 를 가져온다.
  ]
  ```

- #### 서버를 실행시켜 보는 명령어

  - `python manage.py runserver`
  
  - 아주 잘된다.

- #### 데이터베이스 만들기

  - 데이터베이스를 만들고 초기화하자
- 명령어
  
  - `python manage.py migrate`
  
- #### 모델 만들기(Models.py)

  - 모델 : 데이터베이스의 구조도
  - 데이터베이스에 어떤 테이블을 만들고 어떤 컬럼을 가지게 할 것인지 결정해준다.
  - 더불어 해당 컬럼의 제약 조건까지도 모델에서 결정한다.
  - 보통 models.py에 작성. 
  - 클래스 형태로 작성한다.
  - 간단하게 만들어보자

```python
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
```
- #### 데이터베이스에 적용시키기

  - 모델 변경 후 적용시키려면 `migrate` 명령어를 사용해야한다.

  - 이 명령을 사용하려면 polls 앱이 현재 프로젝트에 설치되어 있다고 알려줘야한다.

  - `config/settings.py` 를 열고, `[INSTALLED_APPS]` 변수 제일 윗줄에 polls 앱을 추가해준다.

    ```python
    INSTALLED_APPS = [
        'polls',	# 앱 이름을 적어준다.
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    ```

  - 데이터 베이스 적용 명령어

    - `python manage.py makemigrations polls`

  - 문제가 있는 쿼리인지 판단해보고 싶을 때

    - `python manage.py sqlmigrate polls 0001`

  - 변경사항을 데이터베이스에 반영하기 위한 명령어

    - `python manage.py migrate polls 0001`

  - script

    - ```bash
      python manage.py makemigrations polls
      python manage.py sqlmigrate polls 0001
      python manage.py migrate polls 0001
      ```

  데이터베이스에 테이블을 생성하고, 초기화 완료하였다.

- #### 모델(데이터베이스)에 함수 추가하기

  - [Question] 모델과 [Choice] 모델에 \__\_str___ 메서드 추가
  - 관리자 화면이나 쉘에서 객체 출력 시 나타날 내용을 결정합니다.

  ```python
  from django.db import models
  import datetime
  from django.utils import timezone
  
  # Create your models here.
  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date=models.DateTimeField('date published')
      def __str__(self):
          return self.question_text
      def was_published_recently(self):
          return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  
  class Choice(models.Model):
      question=models.ForeignKey(Question,on_delete=models.CASCADE)
      choice_text=models.CharField(max_length=200)
      votes=models.IntegerField(default=0)
      def __str__(self):
          return self.choice_text
  ```

  - 단순 메서드 변경은 `migrate` 명령어를 사용할 필요가 없다.

- #### 관리자 페이지 확인하기

  - 명령어 : `python manage.py createsuperuser`
  - `~~~/admin`으로 접근 가능하며, 사용자 계정과 그룹만 관리 가능하다.
  - [Question] 모델을 관리하려면 등록해야한다.

- #### admin.py

  ```python
  from django.contrib import admin
  from .models import Question
  
  # Register your models here.
  admin.site.register(Question)	# [Question] 모델을 등록해준다.
  ```

![image](https://user-images.githubusercontent.com/26649731/74306754-c304c100-4da6-11ea-999b-a8f51da9bb84.png)

잘 등록된 것을 볼 수 있다.

- #### 여러가지 뷰 더 추가하기

  - 투표 목록 : 투표 목록 표시 + 상세 페이지 이동 링크
  - 투표 상세 : 투표의 상세 항목 표시
  - 투표 기능 : 선택한 답변에 따라 +1해줌
  - 투표 결과 : 선택한 답변 반영 후 결과 보여줌

- #### polls/views.py (Controller 역할)

  ```python
  from django.shortcuts import render
  from django.http import HttpResponse
  
  # Create your views here.
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      
      # 쿼리들의 질문을 나열한 것들을 합친 결과 : output
      output=', '.join([q.question_text for q in latest_question_list])
      # return HttpResponse("Hello, world. You're at the polls index!!")
      return HttpResponse(output)
  
  # 투표 상세 : 투표의 상세 항목 표시
  def detail(request,question_id):
      return HttpResponse("You're looging at question %s." % question_id)
  
  # 투표 결과 : 선택한 답변 반영 후 결과 보여줌
  def results(request,question_id):
      response = "You're looking at the results of question %s."
      return HttpResponse(response % question_id)
  
  # 투표 기능 : 선택한 답변에 따라 +1해줌
  def vote(request,question_id):
      return HttpResponse("You're voting on question %s." % question_id)
  ```

아직까지는 특별한 기능 없이 값만 출력한다. 

- 뷰가 동작하려면 **URL을 연결**해야한다.

  ```python
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('',views.index,name='index'),
      path('<int:question_id>/',views.detail,name='detail'),
      path('<int:question_id>/results',views.results,name='results'),
      path('<int:question_id>/vote',views.vote,name='vote')
  ]
  ```

  `<int:변수명>` : 값이 변하는 변수를 의미한다.

- `http://127.0.0.1:8000/polls/`를 띄워보면 잘 나온다.

- 하지만 이건 MTV 패턴을 따르지 않았기 때문에 템플릿을 만들어 파이썬 코드와  HTML 코드를 분리해본다.

- #### polls/templates/polls/index.html

  ```html
  <body>
      {% if latest_question_list %}
          <ul>
              {% for question in latest_question_list %}
                  <li><a href="/polls/{{question.id}}/">{{question.question_text}}</a> </li>
              {% endfor %}
          </ul>
      {% else %}
          <p>투표거리가 아직 없습니다.</p>
      {% endif %}
  </body>
  ```

  스파게띠 코드네,, 잘 좀 바꿔봅시다.

  - 만든 템플릿을 이용하려면 **뷰를 변경**해야한다.
  - 템플릿 불러오기 위해 인덱스 함수를 변경해보자.

  ```python
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      context = {
          'latest_question_list':latest_question_list,
      }
  
      # 쿼리들의 질문을 나열한 것들을 합친 결과 : output
      # output=', '.join([q.question_text for q in latest_question_list])
      # return HttpResponse("Hello, world. You're at the polls index!!")
      return render(request,'polls/index.html',context)
  ```

잘 변환되었다.

- views 는 기능을 담당한다.
- 그리고 이걸 의미있게 만드는 것이 `urls.py`이다. 즉, 연결시켜주어야 한다.
- `models.py`는 view 기능을 실행시키기 위한 `VO` 객체이다. 즉, 데이터베이스 부분을 담당하고, 스키마 구성을 돕는다. 보통 `migrate`명령어로 관리된다.

- #### 404 오류 잡아내기

  ```python
  from django.shortcuts import render, get_object_or_404
  
  # 투표 상세 : 투표의 상세 항목 표시
  def detail(request,question_id):
      # 내장함수가 아주 편리하게 되어있다.
      question = get_object_or_404(Question,pk=question_id)
      return render(request,'polls/detail.html',{'question':question})
  ```

- #### namespace 설정하기

  - 분리된 경로를 만드는 개념.

  - `detail` 함수가 polls에도 있고 다른 앱에도 있을 경우 어느 뷰의 url을 만들지 헷갈리기 때문에 설정해야한다.

  - `urls.py`에서 설정해준다.

    ![image](https://user-images.githubusercontent.com/26649731/74313833-c5bbe200-4db7-11ea-891c-ef5a8a6cccac.png)

  - 이럼 끝이기 때문에 `index.html`에서도 설정 바꿔준다.

    ```html
    <a href="/polls/{{question.id}}/">{{question.question_text}}</a>
    <a href="{% url 'polls:detail' question.id %}">{{question.question_text}}</a>
    ```

- #### 제네릭 뷰로 지금까지 한거 무용지물 만들기

  - 장고에서 미리 준비한 뷰.
  - 함수형 뷰 --> 클래스형 뷰

  ```python
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
  ```

  - 클래스형 뷰로 변경 시 `urls.py` 도 변경해줘야 한다.

  ```python
  urlpatterns = [
      # path('',views.index,name='index'),
      # path('<int:question_id>/',views.detail,name='detail'),
      # path('<int:question_id>/results',views.results,name='results'),
      # path('<int:question_id>/vote',views.vote,name='vote')
      path('',views.IndexView.as_view(),name='index'),
      path('<int:pk>/',views.DetailView.as_view(),name='detail'),
      path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
      path('<int:pk>/question_id/vote/',views.vote,name='vote')
  ]
  ```

  - 클래스형 뷰 사용시 `as_view()`를 꼭 사용해주자.



### 후기

- 재미있었던 경험이었다.
- 튜토리얼치고 꽤 괜찮은 프로젝트였다.
- 파이썬 장고의 흐름을 대략적으로 알 수 있었던 좋은 기회였다.