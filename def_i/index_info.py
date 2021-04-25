from django.db import models
from django.db.models import Count, OuterRef, Subquery

from .models import *


class GetIndexInfo:
    def __init__(self, user):
        # 他の情報取得に使うため、進行中のコースを取得
        self.cleared_lesson = ClearedLesson.objects.filter(user=user).order_by('-cleared_at')
        self.last_cleared_lesson = self.cleared_lesson[0]
        next_lesson_num = self.last_cleared_lesson.lesson.lesson_num + 1
        self.learning_lesson = Lesson.objects.get(lesson_num=next_lesson_num)


    # ユーザーのランキング情報を取得
    def get_ranking(self):
        ranking = User.objects.annotate(
            cleared_lesson_num = Subquery(
                ClearedLesson.objects
                    .filter(user=OuterRef('pk'))
                    .values('user')
                    .annotate(count = Count('pk'))
                    .values('count')
            ),
            note_num = Subquery(
                Memo.objects
                    .filter(relate_user=OuterRef('pk'))
                    .values('relate_user')
                    .annotate(count = Count('pk'))
                    .values('count')
            )
            # Noneのとき０にしたい

        ).order_by('-cleared_lesson_num').order_by('-note_num')[:6]  # 何位まで表示する？
        print(ranking)
        return ranking

    # 進捗状況を取得
    def get_progress(self, user):
        all_lesson = Lesson.objects.all().count()
        my_cleared_lesson_num = self.cleared_lesson.count()
        progress_decimal = my_cleared_lesson_num / all_lesson
        progress_percent = progress_decimal * 100
        return progress_percent


    # 進行中のコースに関連した質問を取得
    def get_related_questions(self):
        related_questions = Question.objects.filter(question_at=self.learning_lesson).order_by('-created_at')[:6]
        return related_questions

    # 進行中のコースに関連したノートを取得
    def get_related_articles(self):
        related_articles = Article.objects.filter(article_at=self.learning_lesson).order_by('-created_at')[:6]  # 並べる順番
        return related_articles

    # 進捗が近いユーザーを取得
    def get_colleagues(self, user):
        colleague_data = ClearedLesson.objects.filter(lesson=self.last_cleared_lesson.lesson).exclude(user=user).order_by('-cleared_at')[:6]
        return colleague_data


# お知らせを取得
    def get_notification(self, user):
        # 記事へのいいね
        new_likes = Like.objects.filter(article__poster=user, has_noticed=False)
        print(new_likes)
        # 記事へのコメント
        article_talk = TalkAtArticle.objects.filter(msg_to=user, has_noticed=False).order_by('-time')
        # 質問へのコメント
        question_talk = TalkAtQuestion.objects.filter(msg_to=user, has_noticed=False).order_by('time')

        for like in new_likes:
            like.has_noticed = True
            like.save()
        for talk in article_talk:
            talk.has_noticed = True
            talk.save()
        for talk in question_talk:
            talk.has_noticed = True
            talk.save()

        return new_likes, article_talk, question_talk

        # return new_notifications