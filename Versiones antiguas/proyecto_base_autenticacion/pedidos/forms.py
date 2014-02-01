from django import forms
from models import Usuarios, Pedidos

class UsuariosForm(forms.ModelForm):
	class Meta:
		model = Usuarios

class PedidosForm(forms.ModelForm):
	class Meta:
		model = Pedidos

class LoginForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

