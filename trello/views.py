from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import Board,BoardList,ListCard
from .forms import BoardForm,ListForm,CardForm,UserChangeForm,UserCreationForm
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from .models import Board
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.views.generic.base import View

# Create your views here.
class ViewBoards(LoginRequiredMixin,TemplateView):
    template_name = "trello/board_list.html"
    login_url = '/accounts/login/'

    def get(self,request):
        #import pdb; pdb.set_trace()
        boards = Board.objects.filter(date_created__lte=timezone.now(),user=request.user).order_by('date_created')
        
        return render(request, self.template_name, {'boards':boards})

class AddBoard(LoginRequiredMixin,TemplateView):
    template_name = "trello/board_new.html"
    login_url = '/accounts/login/'
    form = BoardForm

    def get(self,request):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    



class AddBoardAjax(TemplateView):
    template_name = "trello/board_new.html"
    form = BoardForm

    def post(self,request, **kwargs):
        form = self.form(request.POST)

        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return JsonResponse({})
        return JsonResponse({}, status=400)


class EditBoardAjax(TemplateView):
    template_name = "trello/board_edit.html"
    form = BoardForm
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return JsonResponse({'board_form':board_form.title})
        return JsonResponse({}, status=400)




class EditBoard(LoginRequiredMixin,TemplateView):
    template_name = "trello/board_edit.html"
    login_url = '/accounts/login/'
    form = BoardForm

    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(instance=board)
        return render(request, self.template_name, {'form':form,'board_id':board.id})
    
    



class DeleteBoard(LoginRequiredMixin,TemplateView):

    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"), user=request.user)
        board.delete()
        
        return redirect('viewBoards')




class BoardContent(LoginRequiredMixin,TemplateView):
    template_name = "trello/board.html"
    login_url = '/accounts/login/'
    
    def get(self,request, **kwargs):
        board_id = kwargs.get('board_id')
        
        board = get_object_or_404(Board,id=board_id)
        board_lists = BoardList.objects.filter(board_id=board_id)        
        list_cards = ListCard.objects.filter(is_archived=False)
        
        return render(request,self.template_name, {'board':board,'board_lists':board_lists,'list_cards':list_cards,})
        




class AddListAjax(TemplateView):
    template_name = "trello/add_list.html"
    form = ListForm
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            return JsonResponse({'board_form':board_form.title})
        return JsonResponse({}, status=400)


class AddList(LoginRequiredMixin,TemplateView):
    template_name = "trello/add_list.html"
    login_url = '/accounts/login/'
    form = ListForm

    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form()
        return render(request, self.template_name, {'form':form,'board_id':board.id})
    
    


class EditList(LoginRequiredMixin,TemplateView):
    template_name = "trello/edit_list.html"
    login_url = '/accounts/login/'
    form = ListForm
    
    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(instance=board_list)
        
        return render(request, self.template_name, {'form':form,'list_id':board_list.id,'board_id':board.id})


    


class EditListAjax(TemplateView):
    template_name = "trello/edit_list.html"
    form = ListForm
    
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board_list)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            return JsonResponse({})
        return JsonResponse({}, status=400)


class EditCard(LoginRequiredMixin,TemplateView):
    template_name = "trello/edit_card.html"
    login_url = '/accounts/login/'
    form = CardForm

    def get(self,request,**kwargs):
        
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        form = self.form(instance=card)
        return render(request, self.template_name, {'form':form,'board_id':board.id,'list_id':board_list.id,'card_id':card.id})

class EditCardAjax(TemplateView):
    template_name = "trello/edit_card.html"
    form = CardForm
    def post(self,request,**kwargs):
        
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        #board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=card)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return JsonResponse({})
        return JsonResponse({}, status=400)


class ChangeCard(TemplateView):

    def post(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board_list = get_object_or_404(BoardList,id=request.POST.get('id'))
        card.board_list = board_list
        card.save()
        return JsonResponse({}, status=200)

    

class AddCard(LoginRequiredMixin,TemplateView):
    template_name = "trello/add_card.html"
    form = CardForm

    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form()
        return render(request, self.template_name, {'form':form,'board_id':board.id,'list_id':board_list.id})
    

class AddCardAjax(TemplateView):
    template_name = "trello/add_card.html"
    form = CardForm

    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        form = self.form(request.POST)
        
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board_list = board_list
            board_form.save()
            return JsonResponse({})
        return JsonResponse({}, status=400)


class DeleteCard(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.delete()
        
        return redirect('boardContent', board_id=board.id)


class ArchiveCard(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.is_archived = True
        card.save()
        return redirect('boardContent', board_id=board.id)

class CardArchives(LoginRequiredMixin,TemplateView):
    template_name = "trello/archived_cards.html"
    login_url = '/accounts/login/'
    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        archived_cards = ListCard.objects.filter(is_archived=True)

        return render(request,self.template_name, {'archived_cards':archived_cards,'board_id':board.id})
    
        

class RestoreCard(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.is_archived = False
        card.save()
        return redirect('boardContent', board_id=board.id)
    

class DeleteList(LoginRequiredMixin,TemplateView):
    login_url = ''
    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_list.delete()
        
        return redirect('boardContent', board_id=board.id)




class SignUp(TemplateView):
    form = UserCreationForm
    template_name = 'registration/signup.html'

    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.clean_password2()
            form.save()
            return redirect('/accounts/login/')

        return render(request,self.template_name,{'form':form})


class PasswordReset(TemplateView):
    template_name = 'registration/signup.html'

    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.clean_password2()
            form.save()
            return redirect('/accounts/login/')

        return render(request,self.template_name,{'form':form})


    







        
        
        