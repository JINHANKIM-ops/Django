from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# 글의 분류(일상, 유머, 정보)
class Category(models.Model):
    name = models.CharField(max_length=50, help_text="블로그 글의 분류를 입력하세요.(ex:일상)")

    def __str__(self):
        return self.name


# 블로그 글(제목, 작성일, 대표 이미지, 내용, 분류)
class Post(models.Model):
    title = models.CharField(max_length=200)
    title_image = models.ImageField(blank=True, null=True, upload_to="media")
    content = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now_add=True)
    # 하나의 글을 여러가지 분류에 해당될 수 있다.(ex:정보,유머), 하나의 분류에는 여러가지 글이 포함될 수 있다.
    category = models.ManyToManyField(Category, help_text="글의 분류를 설정하세요.")

    def __str__(self):
        return self.title

    # 1번 글의 경우 -> post/1
    def get_absolute_url(self):
        return reverse("post", args=[str(self.id)])

    def is_content_more300(self):
        return len(self.content) > 300

    def get_content_under300(self):
        return self.content[:300]


# 댓글
class PostComment(models.Model):
    # 게시글 Post를 board에 종속, writer는 User모델과 연결
    # get_user_model(): 커스텀 모델, 커스텀 User가 없으면 USER를 받는 메서드
    board = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    # 정렬 순서
    class Meta:
        ordering = ['updated']

    def __str__(self):
        return (self.writer.username if self.writer else "무명") + "의 댓글"



