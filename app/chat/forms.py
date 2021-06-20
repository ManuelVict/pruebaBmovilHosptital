from django  import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import chatUSer,Meet,Message
from django.contrib.auth.forms import AuthenticationForm

class formMeet(forms.ModelForm):
    class Meta:
        model=Meet
        fields=('ccUser','assigDate','ccDoc','state')

class formImage(forms.ModelForm):
    class Meta:
        model=Message
        fields=('image','value')
   

class formLoginUser(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(formLoginUser, self).__init__(*args,**kwargs )
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['username'].widget.attrs['placeholder']='Ingrese Cedula'
        self.fields['password'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['placeholder']='Ingrese Contraseña'
    

class formUserRegister(forms.ModelForm):
    password1=forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Ingrese contraseña',
            'id':'password1',
            'required':'required',
        }
    ))
    password2=forms.CharField(label='Confirmacion', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder':'Ingrese Nuevamente contraseña',
            'id':'password2',
            'required':'required',
        }
    ))
    class Meta:
        model=chatUSer
        fields=('cedula','name','lastName','cellPhone','email','addres','birhtDate','gender')
        

    def clean_password2(self):
        password1 =self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2

    def save(self,commit = True):
        chatUSer=super().save(commit=False)
        chatUSer.set_password(self.cleaned_data.get('password1'))
        if commit:
            chatUSer.save()
        return chatUSer

