from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    username = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'board'
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'

    def __str__(self):
        return self.title
