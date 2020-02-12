- #### init script

  ```bash
  pip install django	# 가상환경에서 장고 설치
  django-admin startproject config .	# config 파일 설치
  python manage.py startapp polls	# 만들고자 하는 앱 생성 cmd
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

  




