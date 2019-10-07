from django.contrib import admin
from django.urls import path,include
from .views import ViewBoards,AddBoard, BoardContent,AddList,EditBoard,AddCard,EditCard,EditList,DeleteCard,DeleteList,DeleteBoard

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
    
]