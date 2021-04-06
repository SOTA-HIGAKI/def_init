from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.shortcuts import resolve_url
from def_init.secret_settings import *
import requests

User = get_user_model()

def get_task():
    category = Task_Sub.objects.get(title='public')
    category_id = category.pk

    return category_id

class Task(models.Model):
    title = models.CharField(max_length=30)
    number = models.PositiveSmallIntegerField(default=0)
    contents = models.TextField(max_length=1000)
    clear = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class Task_Sub(models.Model):
    title = models.CharField(max_length=30)
    number = models.PositiveSmallIntegerField(default=0)
    task_belong = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_sub",default=1)
    clear = models.BooleanField(default=False)


    def __str__(self):
        return str(self.title)


class Article(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_article")
    article_at = models.ForeignKey(Task_Sub, on_delete=models.CASCADE, related_name="task_article", default=get_task)
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    tags = TaggableManager(blank=True)
    # article_image = models.ImageField(upload_to="def_i/img",null=True)
    # article_image_resize = ImageSpecField(source='user_image',
    # processors=[ResizeToFill(250,250)],
    # format='JPEG',
    # options={'quality':60})
    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content)

class Question(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_question")
    question_at = models.ForeignKey(Task_Sub, on_delete=models.CASCADE, related_name="task_question", default=get_task)
    title = models.CharField(max_length=30)
    content = models.TextField(null=True)
    if_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.title)+" by "+str(self.poster)

    def browser_push(self,request):
        data = {
            'app_id':'ea35df03-ba32-4c85-9f7e-383106fb1d24',
            'safari_web_id': "web.onesignal.auto.47a2f439-afd3-4bb7-8cdd-92cc4f5ee46c",
            'included_segments': ['All'],
            'contents': {'en': self.title},
            'headings': {'en': '新しい質問が投稿されました！質問に答えましょう．'},
            'url': resolve_url('question_feed_new'),
        }
        requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers={'Authorization': ONESIGNAL_SECRET_KEY},
            json=data,
        )


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Talk(models.Model):
    msg = models.TextField(max_length=1000)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_form")
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_to")
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{}から{}へのメッセージ".format(self.msg_from,self.msg_to)

#add
class TalkAtArticle(Talk):
    msg_at = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return "FROM '{}' TO '{}' AT '{}'".format(self.msg_from,self.msg_to,self.msg_at)
class TalkAtQuestion(Talk):
    msg_at = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return "FROM '{}' TO '{}' AT '{}'".format(self.msg_from,self.msg_to,self.msg_at)


class Memo(models.Model):
    relate = models.OneToOneField(Task,on_delete=models.CASCADE, related_name="task_memo")
    contents = models.TextField(null=True)
