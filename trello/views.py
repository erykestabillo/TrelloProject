from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import Board,BoardList,ListCard
from .forms import BoardForm,ListForm,CardForm
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from .models import Board


# Create your views here.
class ViewBoards(TemplateView):
    template_name = "board_list.html"

    def get(self,request):
        #import pdb; pdb.set_trace()
        boards = Board.objects.filter(date_created__lte=timezone.now()).order_by('date_created')
        
        return render(request, self.template_name, {'boards':boards})

class AddBoard(TemplateView):
    template_name = "board_new.html"
    form = BoardForm

    def get(self,request):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.date_created = timezone.now()
            board_form.save()
            form.save_m2m()
            return redirect('viewBoards')
            #import pdb; pdb.set_trace()

        return render(request,self.template_name,{'form':form})


class EditBoard(TemplateView):
    template_name = "board_new.html"
    form = BoardForm

    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(instance=board)
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return redirect('boardContent', board_id=board.id)
            #import pdb; pdb.set_trace()

        return render(request,self.template_name,{'form':form})



class DeleteBoard(TemplateView):

    def get(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"), user=request.user)
        board.delete()
        
        return redirect('viewBoards')




class BoardContent(TemplateView):
    template_name = "board.html"

    
    def get(self,request, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board,id=board_id)
        board_lists = BoardList.objects.filter(board_id=board_id)        
        list_cards = ListCard.objects.all()        

        return render(request,self.template_name, {'board':board,'board_lists':board_lists,'list_cards':list_cards,})


class AddList(TemplateView):
    template_name = "add_list.html"
    form = ListForm

    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            
            return redirect('boardContent', board_id=board.id)

        return render(request,self.template_name,{'form':form})


class EditList(TemplateView):
    template_name = "add_list.html"
    form = ListForm

    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        form = self.form(instance=board_list)
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=board_list)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board = board
            board_form.save()
            
            return redirect('boardContent', board_id=board.id)

        return render(request,self.template_name,{'form':form})


class EditCard(TemplateView):
    template_name = "add_card.html"
    form = ListForm

    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        form = self.form(instance=card)
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        form = self.form(request.POST,instance=card)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.user = request.user
            board_form.save()
            return redirect('boardContent', board_id=board.id)
            #import pdb; pdb.set_trace()

        return render(request,self.template_name,{'form':form})



class AddCard(TemplateView):
    template_name = "add_card.html"
    form = CardForm

    def get(self,request,**kwargs):
        form = self.form()
        return render(request, self.template_name, {'form':form})
    
    def post(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        #import pdb; pdb.set_trace()
        form = self.form(request.POST)
        if form.is_valid():
            board_form = form.save(commit=False)
            board_form.board_list = board_list
            board_form.save()
            
            return redirect('boardContent', board_id=board.id)

        return render(request,self.template_name,{'form':form})


class DeleteCard(TemplateView):

    def get(self,request,**kwargs):
        card = get_object_or_404(ListCard,id=kwargs.get("card_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        card.delete()
        
        return redirect('boardContent', board_id=board.id)
    

class DeleteList(TemplateView):

    def get(self,request,**kwargs):
        board_list = get_object_or_404(BoardList,id=kwargs.get("list_id"))
        board = get_object_or_404(Board,id=kwargs.get("board_id"))
        board_list.delete()
        
        return redirect('boardContent', board_id=board.id)





    







        
        
        