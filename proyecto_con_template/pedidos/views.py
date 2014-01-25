from django.shortcuts import render
from django.template import RequestContext, loader
from pedidos.models import Usuarios, Pedidos
from forms import UsuariosForm, PedidosForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect

# Create your views here.

# LLODRA
def index(request):
	return render(request,'pedidos/index.html')

# FRAN
def alta_usuario(request):
    if request.POST:
        form = UsuariosForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ingenia/')
    else:
        form = UsuariosForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/crear_usuario.html',args)

# FRAN
def asignar_pedido(request):
	if request.POST:
		form = PedidosForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/ingenia/')
	else:
		form = PedidosForm()

	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'pedidos/asignar_pedido.html',args)

#
def administrar(request):
    return render(request,'pedidos/administrar.html')
    
# JUAN
def estado_pedido(request):
	return render(request,'pedidos/estado_pedido.html') 
 
 
# RAFA 
def actualizar_pedido(request):
	return render(request,'pedidos/actualizar_pedido.html')
