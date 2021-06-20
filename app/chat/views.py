from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import CreateView,TemplateView,View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import chatUSer, Meet, Room, Message
from .forms import formUserRegister,formLoginUser,formMeet,formImage
from .mixins import SuperUSerMixin,IsLogin
from .serializers import RoomSerializer,MessageSerializer

# Create your views here.
def logoutView(request):
    logout(request)
    return render(request,'logoutmain.html')


def index(request):
    print(request.user.id)
    meets=Meet.objects.filter(ccUser=request.user.id)
    print(meets)
    return render( request, 'index.html',{'meets':meets})




class MeetRegister(LoginRequiredMixin,SuperUSerMixin,CreateView):
    model=Meet
    form_class=formMeet
    template_name='meet.html'
    success_url=reverse_lazy('index')

class usuarioRegister(IsLogin,CreateView):
    model = chatUSer
    form_class = formUserRegister
    template_name= 'register.html'
    success_url = reverse_lazy('login')

class SendImages(LoginRequiredMixin,CreateView):
    model=Message
    form_class=formImage
    template_name='upploadimage.html'
    success_url = reverse_lazy('chat')
   


class Login(IsLogin,FormView):
    template_name='login.html'
    form_class=formLoginUser
    success_url=reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request, *args, **kwargs):
        print("pase")
        print(request.user)
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)
    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

def room(request,room):
    username=request.user.name
    roomDetails= Room.objects.get(name=room)
    print(Room.objects.get(name=room))
    return render(request, 'room.html',{
        'username':username,
        'room':room,
        'roomDetails':roomDetails,
    })

def chat(request):
    return render(request,'chat.html')

def checkview(request):
    room=request.POST['room_name']
    username=request.user.name
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        newRoom = Room.objects.create(name=room)
        newRoom.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message= request.POST['message']
    username= request.user.id
    idRom= request.POST['idRom']

    newMessage = Message.objects.create(value=message, user=username, room=idRom)
    newMessage.save()
    return HttpResponse("message sent")


def getMessages(request,room):
    roomDetails = Room.objects.get(name=room)
    messages = Message.objects.filter(room=roomDetails.id)
    mesaje= Room.objects.all()

    return JsonResponse({"messages":list(messages.values())})

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset=RoomSerializer.Meta.model.objects.all()

class MessaggeViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset=MessageSerializer.Meta.model.objects.all()

    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'mensaje añadido'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first() # get instance        
        if product:
            product.state = False
            product.save()
            return Response({'message':'Producto eliminado correctamente!'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un Producto con estos datos!'},status = status.HTTP_400_BAD_REQUEST)
   
   



 



    
        