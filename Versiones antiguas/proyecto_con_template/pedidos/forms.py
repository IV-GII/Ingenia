from django import forms
from models import Usuarios, Pedidos

class UsuariosForm(forms.ModelForm):
	class Meta:
		model = Usuarios

class PedidosForm(forms.ModelForm):
	class Meta:
		model = Pedidos
