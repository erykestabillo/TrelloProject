from django.forms import ModelForm
from .models import Board,BoardList, ListCard

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title']


class ListForm(ModelForm):
    class Meta:
        model = BoardList
        fields = ['title']


class CardForm(ModelForm):
    class Meta:
        model = ListCard
        fields = ['title']