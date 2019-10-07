from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.date_created = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class BoardList(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class ListCard(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    board_list = models.ForeignKey(BoardList, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title






