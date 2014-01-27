from django.shortcuts import render
from django.template import RequestContext, loader
from pedidos.models import Usuarios, Pedidos
from forms import UsuariosForm, PedidosForm, LoginForm, EstadosForm, SearchPedidoForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Create your views here.

# LLODRA
def index(request):
    request.session['usuario'] = ''
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                m = Usuarios.objects.get(nombre__exact=request.POST['nombre'])
                if m.password == request.POST['password']:
                    request.session['usuario'] = m.nombre
                    if m.rol == 'Cliente':
                        return HttpResponseRedirect('/ingenia/estado_pedido/')
                    else:
                        return HttpResponseRedirect('/ingenia/administrar/')
                    
                else:
                    return HttpResponseRedirect('/ingenia/')
            except Usuarios.DoesNotExist:
                return HttpResponseRedirect('/ingenia/')
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
    usuario = request.session["usuario"]
    if usuario != '':    
        if request.POST:
            form = UsuariosForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/ingenia/administrar')
        else:
            form = UsuariosForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            return render(request,'pedidos/crear_usuario.html',args)
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args) 
        
# FRAN
def asignar_pedido(request):
    usuario = request.session["usuario"]
    if usuario != '': 
        if request.POST:
		form = PedidosForm(request.POST)
		if form.is_valid():
                  form.save()     
                  return HttpResponseRedirect('/ingenia/administrar/')
	else:
		form = PedidosForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'pedidos/asignar_pedido.html',args)
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args) 
        
# FRAN
def administrar(request):    
    usuario = request.session["usuario"]
    if usuario != '':
        return render(request,'pedidos/administrar.html',{"usuario":usuario})
    else:        
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args) 

# FRAN
def admin_estados(request):
    usuario = request.session["usuario"]
    if usuario != '':
        if request.POST:
            form = EstadosForm(request.POST)
            if form.is_valid():
                form.save()     
                return render(request,'pedidos/administrar.html')
        else:
            form = EstadosForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            return render(request,'pedidos/admin_estados.html',args)
    else:        
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)     

# FRAN
def cerrar_sesion(request):
    request.session["usuario"]=''
    form = LoginForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request,'pedidos/index.html',args)  
    
# JUAN
def estado_pedido(request):
    usuario = request.session["usuario"]
    if usuario != '':       
        lista_pedidos = Pedidos.objects.filter(usuario='3')
        context = {'lista_pedidos' : lista_pedidos}
        return render(request,'pedidos/estado_pedido.html', context) 
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)             

# RAFA 
def actualizar_pedido(request):
    usuario = request.session["usuario"]
    if usuario != '': 
        lista_estado1 = Pedidos.objects.filter(estado=1)
        lista_estado2 = Pedidos.objects.filter(estado=2)
        lista_estado3 = Pedidos.objects.filter(estado=3)
        lista_estado4 = Pedidos.objects.filter(estado=4)
        lista_estado5 = Pedidos.objects.filter(estado=5)
        lista_estado6 = Pedidos.objects.filter(estado=6)
        lista_estado7 = Pedidos.objects.filter(estado=7)
        lista_estado8 = Pedidos.objects.filter(estado=8)
        if request.method == 'POST':
            form = SearchPedidoForm(request.POST)
            if form.is_valid():  
                npedidos = form.data['num_pedido']
                nestado = form.data['estado']
                Pedidos.objects.filter(num_pedido = npedidos).update(estado = nestado)
                return render(request,'pedidos/actualizar_pedido.html', {'form' : form,'lista_estado1': lista_estado1, 'lista_estado2': lista_estado2,'lista_estado3': lista_estado3,'lista_estado4': lista_estado4,'lista_estado5': lista_estado5, 'lista_estado6': lista_estado6, 'lista_estado7': lista_estado7, 'lista_estado8': lista_estado8})
        else:
            form = SearchPedidoForm()
        return render(request,'pedidos/actualizar_pedido.html', {'form' : form,'lista_estado1': lista_estado1, 'lista_estado2': lista_estado2,'lista_estado3': lista_estado3,'lista_estado4': lista_estado4,'lista_estado5': lista_estado5, 'lista_estado6': lista_estado6, 'lista_estado7': lista_estado7, 'lista_estado8': lista_estado8})
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)  