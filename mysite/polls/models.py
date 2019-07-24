import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Searching DB Model
class Search(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    cprice = models.IntegerField(default=0)
    industry_code = models.CharField(max_length=20, default='')     # 업종코드 (외부 업종명과 연결시켜야함)
    industry_name = models.CharField(max_length=20, default='')
    diff = models.IntegerField(default=0)
    last_update = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.name


"""
class Upjong(models.Model):
    industry_cd = models.ForeignKey(Search, on_delete=models.CASCADE)
    industry_name = models.CharField(max_length=20)

    def __str__(self):
        return self.industry_name
"""

