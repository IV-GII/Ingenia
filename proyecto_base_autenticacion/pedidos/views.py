from django.shortcuts import render
from django.template import RequestContext, loader
from pedidos.models import Usuarios, Pedidos
from pedidos.forms import LoginForm
from forms import UsuariosForm, PedidosForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Create your views here.

# LLODRA
def index(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                m = Usuarios.objects.get(nombre__exact=request.POST['nombre'])
                if m.password == request.POST['password']:
                    return HttpResponse("You're logged in.")
                else:
                    return HttpResponse("password incorrecta.")
            except Usuarios.DoesNotExist:
                return HttpResponse("Your username and password didn't match.")
            
            
        else:
            form = LoginForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            return render(request,'pedidos/index.html',args)

    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)

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

# RAFA
def estado_pedido(request):
	return render(request,'pedidos/estado_pedido.html') 
 
 
# JUAN 
def actualizar_pedido(request):
	return render(request,'pedidos/actualizar_pedido.html')
 