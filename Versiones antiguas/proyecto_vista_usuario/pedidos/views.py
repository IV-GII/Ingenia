from django.shortcuts import render
from django.template import RequestContext, loader
from pedidos.models import Usuarios, Pedidos
from forms import UsuariosForm, PedidosForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response




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

def asignar_pedido(request):
	if request.POST:
		form = PedidosForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/ingenia/')
	else:
		form = UsuariosForm()

	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'pedidos/asignar_pedido.html',args)

#juan
def estado_pedido(request):
	lista_pedidos = Pedidos.objects.filter(usuario=3)
	context = {'lista_pedidos' : lista_pedidos}
	return render(request,'pedidos/estado_pedido.html', context)
  
 

def actualizar_pedido(request):
	return render(request,'pedidos/actualizar_pedido.html')
 
