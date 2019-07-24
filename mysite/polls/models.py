import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# 장고 예제
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


# 장고 예제
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Searching DB Model (Stock DB table Instance)
class Search(models.Model):
    code = models.CharField(max_length=20)                          # 종목 코드
    name = models.CharField(max_length=20)                          # 종목 명
    cprice = models.IntegerField(default=0)                         # 현재가 (장 마감시 종가)
    industry_code = models.CharField(max_length=20, default='')     # 업종코드 (외부 업종명과 연결시켜야함)
    industry_name = models.CharField(max_length=20, default='')     # 업종명 (결국 연결시키지 못하였다.)
    diff = models.IntegerField(default=0)                           # 전일대비
    last_update = models.TimeField(default=timezone.now)            # 갱신시각 (Django time format = HH:MM)

    def __str__(self):
        return self.name


