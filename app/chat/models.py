from datetime  import datetime 
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
# Create your models here.

class chatUserManager(BaseUserManager):
    def createUser(self, cedula,email,name,lastName,password=None):
        if not cedula:
            raise ValueError('El usuario debe tener una cedula')
            print("pase por aqui")


        chatUSer= self.model(
            cedula=cedula,
            email=self.normalize_email(email),
            name=name,
            lastName=lastName,
        )
        print("pase por aqui")
        chatUSer.set_password(password)
        chatUSer.save()
        return chatUSer

    def create_superuser(self, cedula,email,name,lastName,password=None):
        chatUSer= self.createUser(
            cedula,
            email=self.normalize_email(email),
            name=name,
            lastName=lastName,
            password=password
        )
        chatUSer.isAdmin=True
        chatUSer.save()
        return chatUSer

class chatUSer(AbstractBaseUser):
    cedula=models.CharField("Cedula",unique=True,max_length=20)
    name=models.CharField(max_length=100, help_text="Ingrese su nombre")
    lastName=models.CharField(max_length=100, help_text="Ingrese su apellido")
    cellPhone=models.BigIntegerField(help_text="Ingrese su Celular",blank=True, null=True)
    email=models.EmailField(max_length=200,help_text="Ingrese su email")
    addres=models.CharField(max_length=200, help_text="Ingrese su direcció",blank=True, null=True)
    birhtDate=models.DateTimeField(blank=True, null=True)
    gender=models.CharField(max_length=1, help_text="M -> Masculino, F-> Femenino, O ->Otro",blank=True, null=True)
    isAdmin=models.BooleanField(default=False)
    objects=chatUserManager()

    USERNAME_FIELD='cedula'
    REQUIRED_FIELDS=['email','name','lastName']
    
    def __str__(self):
        return f'{self.cedula},{self.name},{self.lastName}'
     
    def has_perm(self,perm,ob =None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.isAdmin


    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
        db_table= 'chatUser'


class Meet(models.Model):
    checkIn= 'CI'
    checkOut= 'CO'
    canceled= 'CD'
    attended= 'AT'

    possibleStates=(
        (checkIn, 'Check-in'),
        (checkOut,'Check-out'),
        (canceled, 'Cancelada'),
        (attended, 'asistio'),
    )

    idMeet=models.AutoField(auto_created=True,primary_key=True)
    ccUser = models.ForeignKey(chatUSer, on_delete=models.SET_NULL,related_name='usario', null=True)
    assigDate=models.DateTimeField()
    toDay=models.DateTimeField(default=datetime.now, blank=True)
    ccDoc=models.BigIntegerField()
    state=models.CharField(max_length=2,choices=possibleStates)
    

    def __str__(self):
        return str(self.idMeet)

    class Meta:
        verbose_name='meet'
        verbose_name_plural='meets'
        db_table= 'meet'





class Room(models.Model):
    name=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name='room'
        verbose_name_plural='rooms'
        db_table= 'room'



class Message(models.Model):
    value=models.CharField(max_length=10000000,blank=True)
    date=models.DateTimeField(default=datetime.now)
    user=models.CharField(max_length=1000000)
    room=models.CharField(max_length=100000)
    image=models.ImageField(upload_to="images/",null=True, blank=True)
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name='message'
        verbose_name_plural='messages'
        db_table= 'message'



     