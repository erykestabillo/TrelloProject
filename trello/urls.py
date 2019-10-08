from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView

from .views import (ViewBoards,
                    AddBoard, 
                    BoardContent,
                    AddList,EditBoard,
                    AddCard,
                    EditCard,
                    EditList,
                    DeleteCard,
                    DeleteList,
                    DeleteBoard,
                    SignUp,
                    AddBoards,)

urlpatterns = [
    path('', ViewBoards.as_view(), name="viewBoards"),
    path('board/new', AddBoard.as_view(), name="addBoard"),
    path('board/<int:board_id>/edit', EditBoard.as_view(), name="editBoard"),
    path('board/<int:board_id>/delete', DeleteBoard.as_view(), name="deleteBoard"),
    path('board/<int:board_id>', BoardContent.as_view(), name="boardContent"),
    path('board/<int:board_id>/list/new', AddList.as_view(), name="addList"),
    path('board/<int:board_id>/<int:list_id>/edit', EditList.as_view(), name="editList"),
    path('board/<int:board_id>/<int:list_id>/delete', DeleteList.as_view(), name="deleteList"),
    path('board/<int:board_id>/<int:list_id>/add', AddCard.as_view(), name="addCard"),
    path('board/<int:board_id>/<int:list_id>/<int:card_id>/edit', EditCard.as_view(), name="editCard"),
    path('board/<int:board_id>/<int:list_id>/<int:card_id>/delete', DeleteCard.as_view(), name="deleteCard"),
    
    path('accounts/signup/', SignUp.as_view(), name='signUp'),
    path('accounts/password_reset/', PasswordResetView.as_view(), name='passwordReset'),

     path('board/new/ajax/', AddBoards.as_view(), name="addBoards"),
    
]