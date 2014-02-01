from django import forms
from models import Usuarios, Pedidos

class UsuariosForm(forms.ModelForm):
	class Meta:
             password = forms.CharField(widget=forms.PasswordInput)
             model = Usuarios
             widgets = {
                 'password': forms.PasswordInput(),
             }

class PedidosForm(forms.ModelForm):
	class Meta:
		model = Pedidos

class LoginForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)