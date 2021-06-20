from django.urls import  path
from . import views

urlpatterns=[
   # path('login/', views.login, name='login'),
    path('register/', views.usuarioRegister.as_view() ,name='register'),
    path('meet/',views.MeetRegister.as_view(),name='meet'),
    

]