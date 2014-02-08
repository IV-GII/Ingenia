IngeniaTracking
===============

Servicio tracking para empresa de imprenta (Ingenia):

<center>![captura_logo_empresa](https://dl.dropbox.com/s/rjlmw7zqkq8kw49/logo.jpg)</center>

Francisco Valverde Villalba<br>
Juan Moral Fernandez<br>
Rafael Carrasco Ruiz<br>
Fernando Llodra Belda<br>


Introducción
============

Lo primero que hicimos para desarrollar la aplicación de Ingenia Tracking fué pedir a Melesio (Director Gerente de la empresa Ingenia Digital) una cita para que nos hablara un poco de más de la empresa. El, nos ofreció ir en persona a ver como trabajan en Ingenia Digital asi que aceptamos obviamente. Una vez allí recopilamos información acerca de la estructura de la empresa, el flujo de trabajo, disponibilidad de servidores en caso de necesitarlos y ultimamos detalles sobre que se pedía para la aplicación que ibamos a desarrollar.
Hemos plasmado en nuestra aplicación, según los requisitos de Ingenia Digital, como funciona todo el proceso de trabajo en la empresa y para ello hemos creado una plataforma que servirá tanto para que los trabajadores de la empresa ingenia puedan acceder y administrar usuarios y pedidos, como para los clientes, pudiendo éstos entrar en la plataforma también con el simple permiso de poder ver como se encuentra su pedido (en que fase de desarrollo está).



Puesta a punto de Ingenia Tracking
==================================

Despues de pensar detenidamente en que lenguaje trabajar, preguntándonos los pros y contras de cada uno nos decantamos por python, concretamente en el framework django por varios motivos:
- Es el framework para Python más usado<br>
- Esta enfocado a sitios basados en bases de datos<br>
- Open Source<br>
- Arquitectura: Modelo, Vista, Template

El siguiente paso es realizar la creación de un proyecto donde correrá nuestra aplicación. No es una tarea para realizar a la ligera ya que tuvimos que realizar hasta cuatro veces los siguientes pasos debidos a problemas con las bases de datos en el que la única solución que encontramos era trasladar el proyecto a un nuevo proyecto. Este proceso se automatizo con recetas realizadas en chef que posteriormente mostraremos.

Pasos para crear la aplicación Ingenia Tracking
-----------------------------------------------

1 - Crear un proyecto
~~~~~~{.python}
 virtualenv ENV1  # crea un entorno virtual
 cd ENV1
 source bin/activate
 pip install Django  # instala django 
 django-admin.py startproject ingenia  # crea el proyecto
 cd ingenia/
~~~~~~
2 - Crear una aplicación dentro del proyecto
~~~~~~{.python}
 python manage.py runserver  # Funciona!
 python manage.py syncdb  # mira INSTALLED_APP y crea las tablas necesarias para cada uno de los programas.
 python manage.py startapp pedidos  # crea la aplicación pedidos
~~~~~~
3 - Definir la Base de Datos<p>
Crearemos para esta primera aproximación cuatro tablas (Cliente, Pedidos, Estado, EstadosPedidos), como ya se ha comentado previamente es necesario tener claro este aspecto porque cualquier modificación nos ha provocado volver a realizar estos pasos para que funcione bien.<br>
Cliente será la tabla que contenga la información relacionada con los clientes que han realizado un pedido. Estos clientes son dados de alta por un personal de la empresa.<br>
Pedidos mantendrá todos los pedidos que se han realizado asociandolos a un usuario para que este pueda consultarlos y pueda ver el estado de su pedido.<br>
Estado es la tabla donde aparecen todos los estados por los que pasa un pedido hasta llegar a completado.<br>
EstadosPedidos es una tabla que nos sirve de unión para posteriores consultas</p>
4 - Definir el modelo en app/models.py
~~~~~~{.python}
 nano pedidos/models.py  # Es el archivo donde se diseñan las tablas de la base de datos
 
 class Usuarios (models.Model):
    nombre = models.CharField (max_length=100)
    correo_electronico = models.CharField (max_length=300)
    password = models.CharField (max_length=30)
    rol = models.CharField (max_length=30)
    
 class Estados (models.Model):
    nombre_estado = models.CharField (max_length=30)
    
 class Pedidos (models.Model):
    usuario = models.ForeignKey (Usuarios)
    num_pedido = models.CharField (max_length=15)
    concepto = models.CharField(max_length=200)
    estado = models.ForeignKey (Estados)
    telefono_tecnico = models.CharField (max_length=12, blank=True)
    forma_de_recepcion = models.CharField (max_length=30, blank=True)
        
class EstadosPedidos (models.Model):
    num_pedido = models.ForeignKey (Pedidos)
    estado = models.ForeignKey (Estados)
~~~~~~
5 - Añadir los módulos en settings.py
~~~~~~{.python}
 nano ingenia/settings.py  # para añadir pedidos en INSTALLED_APPS
 
 INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pedidos',
 )
~~~~~~
6 - Crear la Base de Datos
~~~~~~{.python}
 python manage.py sql pedidos
 python manage.py syncdb  # se crea la BD
~~~~~~
7 - Crear los mappings para las urls en urls.py<p>
Lo primero que debemos saber es qué queremos decir cuando hablamos de vistas. Vista o función de vista es una función de Python que toma como argumento una petición web (request) y devuelve una respuesta (response). Es la forma que tiene django de trabajar es por ello que hay que mapear las urls para que realice la redirección de URLs a vistas.
~~~~~~{.python}
# Redireccionamos todos las urls que empiecen por ingenia al archivo pedidos.urls que contiene el mapeo a las vistas.
urlpatterns = patterns('',
    # Examples:
    url(r'^ingenia/', include('pedidos.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
~~~~~~
8 - Definir las vistas en pedidos/views.py
<p>
Las vistas son clases que son usadas cuando se introduce una url y el archivo urls.py redirecciona a una de las clases que se encuentran en el archivo view.py. Son en estas clases donde nace la mágia y se realizan todas las operaciones para que despues se sirva el contenido en el navegador web.<br>
Es es necesario realizar la importación de el paquete template para poder hacer uso de las plantillas
~~~~~~{.python}
from django.shortcuts import render
from django.template import RequestContext, loader
~~~~~~
Una vez se haya trabajado con los datos se renderizan estos datos a un archivo .html para que se muestren los datos con aspecto atractivo.<br>
En las siguientes secciones veremos mas de cerca cada vista.</p>


Página de Logeo
===============

Nada más entrar a la aplicación aparece un formulario de logeo ![screenshot](http://dl.dropboxusercontent.com/s/t0rrvxr8j7ygph6/Captura%20de%20pantalla%202014-02-04%20a%20la%28s%29%2021.51.24.png) en el que nos podremos logear ya seamos clientes o trabajadores, y dependiendo del rol se tendrá una siguiente vista u otra. Para el Trabajador, la vista consistirá en un panel donde podremos dar de alta a un usuario, asignarle un pedido o actualizar el estado de un pedido. Para el Cliente, simplemente se mostrarán sus pedidos con la información de éste tal que: nº de pedido, descripción, estado, porcentaje de progreso del pedido, un número de contacto y si la entrega se hace a domicilio o viene el cliente a recogerlo.

Para el logeo hemos usado el siguiente código:

~~~~~~{.python}
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
~~~~~~


Alta de usuario
===============
Esta vista solo se podrá acceder su eres un trabajador de la empresa. Una vez que el cliente solicita el seguimiento de su pedido, uno de los trabajadores de la empresa Ingenia le dará de alta en el sistema, facilitándole un usuario y una contraseña de acceso.<br><br>
Esta es la apariencia que cuenta el alta de usuario:

![captura_alta](https://dl.dropbox.com/s/6dqdhta5crp1wgf/alta_user.png)

Como se puede apreciar se trata de un simple formulario que una vez que sea valido sus entradas se añadirá una nueva fila a la tabla de usuarios.

Para poder mostrar un formulario en django se debe generar una clase especifica en el archivo forms.py de la carpeta de nuestra aplicación. En este caso como vamos a usar todos los campos de la tabla podemos hacerlo tal que así:
~~~~~~{.python}
class UsuariosForm(forms.ModelForm):
<<<<<<< HEAD
    class Meta:
=======
	class Meta:
>>>>>>> ccc162b7011f9f07f28a390318f1a7ea12b95eb0
             password = forms.CharField(widget=forms.PasswordInput)
             model = Usuarios
             widgets = {
                 'password': forms.PasswordInput(),
             }
~~~~~~
Asignar Pedido a usuario
========================
La vista de asignar pedido es de solo acceso para los trabajadores, esto al igual en otras vistas de la parte de administración se ha restringido mediante sesiones de usuario donde dependiendo el rol del usuario tendrá acceso a una zona u a otra. Esta clase se encarga de mostrar un formulario para dar de alta pedidos asignandolos a usuarios ya dados de alta en la plataforma. Además de indicarle otros datos como el estado del pedido, el concepto, etc.

![captura_asigna](https://dl.dropbox.com/s/bslwg163133rspb/asigna_pedido.png)

Para poder mostrar un formulario en django se debe generar una clase especifica en el archivo forms.py como ya se ha comentado previamente. En este caso al igual que en alta de usuario se van a usar todos los campos por lo que la clase queda de la siguiente manera:
~~~~~~{.python}
class PedidosForm(forms.ModelForm):
<<<<<<< HEAD
    class Meta:
        model = Pedidos
=======
	class Meta:
		model = Pedidos
>>>>>>> ccc162b7011f9f07f28a390318f1a7ea12b95eb0
~~~~~~

Actualización de pedidos
========================

Esta es una vista solamente para los trabajadores de la empresa. Desde aquí los diferentes trabajadores de las distintas secciones de la empresa, cambiaran el estado del pedido según donde este se encuentre.

La apariencia de actualizar pedido es la siguiente:

![captura_update](https://dl.dropbox.com/s/5d6y6sm3rkraoh9/AcEs.jpg)

Se trata de un simple formulario, con el cual pueden ir cambiando el estado del pedido. Para ello el pedido tiene que estar inicializado en la aplicación, esta operación se realiza desde la vista asignar pedido. 
Solamente necesitamos indicar el número del pedido que queremos cambiar y el nuevo estado al que queremos pasar el pedido y pulsamos actualizar para que la acción se complete.

Otra opción que contiene este apartado es la de enviar un correo electrónico, se puede ver en el código “.py”. Cuando el pedido pasa al estado completado, será enviado un correo al cliente indicado que su pedido está finalizado. 

Se ha utilizado el siguiente código:

Documento .py:

~~~~~~{.python}
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
        lista_estado9 = Pedidos.objects.filter(estado=9)
	
        if request.POST:
            form = SearchPedidoForm(request.POST)
            if form.is_valid():
		 npedidos = form.data['num_pedido']
		 nestado = form.data['estado']
		 Pedidos.objects.filter(num_pedido = npedidos).update(estado = nestado)
		 e = Pedidos.objects.filter(estado=9)
		 for datos in e:
		    asunto = "Ingenia Digital. Pedido: " + datos.concepto
		    men = "<h3>Ingenia Tracking:</h3>Estimado " + datos.usuario.nombre + ". <br> Su pedido con referencia: " + datos.num_pedido + " ha pasado al estado: Completo <br><br><hr>Ingenia Digital <br> Phone: (+34) 958 430 175 - Email: pedidos@ingenia-digital.com <br> Twitter: @Ingenia_Digital - Google plus: https://plus.google.com/+Ingenia-digital"
		    mensaje = """ <html> <body> %s </body> </html>""" % (men)
		    email = EmailMultiAlternatives(asunto, mensaje, to = [datos.usuario.correo_electronico])
		    email.attach_alternative(mensaje, "text/html")
		    email.send()
		 return render(request,'pedidos/actualizar_pedido.html', {'form' : form, 'lista_estado1': lista_estado1, 'lista_estado2': lista_estado2,'lista_estado3': lista_estado3,'lista_estado4': lista_estado4,'lista_estado5': lista_estado5, 'lista_estado6': lista_estado6, 'lista_estado7': lista_estado7, 'lista_estado8': lista_estado8, 'lista_estado9': lista_estado9})
        else:
	  form = SearchPedidoForm()
	return render(request,'pedidos/actualizar_pedido.html', {'form' : form, 'lista_estado1': lista_estado1, 'lista_estado2': lista_estado2,'lista_estado3': lista_estado3,'lista_estado4': lista_estado4,'lista_estado5': lista_estado5, 'lista_estado6': lista_estado6, 'lista_estado7': lista_estado7, 'lista_estado8': lista_estado8, 'lista_estado9': lista_estado9})
      
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)
~~~~~~

Documento .html:

Forma de mostrar un estado.

~~~~~~{.html}
<div class="panel-heading">
	<a class="panel-title" data-toggle="collapse" data-parent="#panel-854654">Revisión</a>
</div>
	<div id="panel-element-590421" class="panel-collapse collapse in">
	{% if lista_estado1 %}							
	     
	      {% for npe in lista_estado1 %}
			<div class="panel-body">
			    <b>Número Pedido:</b> {{ npe.num_pedido }}
			    <b>Cliente:</b> {{ npe.usuario }}
			    <b>Concepto:</b> {{ npe.concepto }}
			    <b>Recepción:</b>{{ npe.forma_de_recepcion }}
			</div>
		{% endfor %}
		
	{% else %}
		<div class="panel-body">
			<p>No existen pedidos en este estado.</p>				
		</div>
	{% endif %}
										
	</div>
</div>
~~~~~~

Vista de cliente
=================

En está página se muestra el estado de los pedidos de un usuario en concreto. Cuando un usuario tipo "cliente" se loguea, accede directamente a esta vista, en la que se muestra información de cada uno de los pedidos que el usuario ha encargado a la empresa. A continuación se detalla cada uno de los campos informativos:

  - Nº de pedido: Número de identificación del pedido
  - Descripción: Breve descripción del pedido en concreto, que facilita la distinción entre ellos.
  - Estado: Situación actual en la que se encuentra el pedido. Los diferentes estados que pueden darse son (por orden de             ascendente): Revisión, Pte entrada producción, Producción, Pte empaquetar, Pte instalación, Listo Recogida,             Listo transporte, Instalación terminada, Completo.
  - % Completado: Dependiendo del estado del pedido, muestra el % de realización de éste a través de una barra de                         estado.
  - Contacto técnico: Cuando un estado necesita la instalación de un profesional de la empresa, se muestra un número de                       contacto para poder establecer una cita personalmente con la persona encargada. 
  - Entrega: Detalles sobre la entrega del pedido, ya sea a través de un servicio de transporte o recogida en la                     empresa. 

Aquí tenemos una muestra de la vista de la página, en la que podemos observar los campos antes mencionados:

![im1](https://dl.dropbox.com/s/6xrdo6f5pq6lb0l/Nueva%20imagen%20%283%29.bmp)

Como se muestra en la imagen anterior, la página también proporciona el nombre del cliente logueado junto a la opción de cerrar sesión.

Para hacer posible esta página, se necesita la función estado_pedido, que se encuentra dentro de views.py. El código de esta función es el siguiente:

~~~~~~{.python}
def estado_pedido(request):
    usuario = request.session["usuario"]
    if usuario != '':
        no_encontrado = True
        id_usuario=1
        while no_encontrado:
            m = Usuarios.objects.get(id=id_usuario)
            if m.nombre == usuario:
                no_encontrado = False 
            else:
                id_usuario = id_usuario + 1
        lista_pedidos = Pedidos.objects.filter(usuario=id_usuario)
        context = {'lista_pedidos' : lista_pedidos, "usuario": usuario}
        return render(request,'pedidos/estado_pedido.html', context) 
        
    else:
        form = LoginForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request,'pedidos/index.html',args)      
~~~~~~




Alojamiento con Windows Azure
=============================

Una vez terminado todo el proceso de programación de nuestra aplicación Ingenia Tracking vamos a crear una máquina virtual en Windows Azure usandola como servidor para nuestra aplicación.

Primero crearemos una máquina virtual Ubuntu 12.04 (puede ser cualquier imagen que se desee). Una vez creada, establecemos los extremos de la misma para la comunicación con ella por medio de ssh y para la ejecución de la aplicación por http.

![screenshot1](http://dl.dropboxusercontent.com/s/ou8y3a2zd9r3hm9/Captura%20de%20pantalla%202014-02-05%20a%20la%28s%29%2012.04.53.png)

Como aparece en la imagen, usaremos los puertos público y privado numero 22 para el extremo ssh y para el http el público 80 y el privado 8000. Ahora solo queda conectarnos por medio del ssh y aprovisionar la maquina para la correcta ejecución de Igenia Tracking. Entramos como ya vimos con el comando
`ssh ubuntu1204peq.cloudapp.net`. A continuación, creamos un entorno solo para nuestra aplicación, instalaremos en el python, django y git (para descargar nuestro repositorio donde tenemos el código fuente de la Ingenia Tracking).

```
sudo apt-get install git
virtualenv IngeniaTracking  # crea un entorno virtual
cd IngeniaTracking
source bin/activate
pip install Django  # instala django 
```
Ahora simplemente entramos en el directorio de nuestra app y ejecutamos `python manage.py runserver 0.0.0.0:8000 &`. 

**Nota:** He tenido que hacer uso del comando `screen` para poder dejar la aplicación corriendo con django en la maquina virtual una vez terminada la comunicación por ssh.

Ya podemos cerrar la comunicación con la maquina virtual de Azure y comprobamos que nuestra aplicación funciona perfectamente en la URL [http://ubuntu1204peq.cloudapp.net/ingenia/](http://ubuntu1204peq.cloudapp.net/ingenia/).

![screenshot2](http://dl.dropboxusercontent.com/s/t0rrvxr8j7ygph6/Captura%20de%20pantalla%202014-02-04%20a%20la%28s%29%2021.51.24.png)




Copyright 2014 Fernando Llodra Belda, Francisco Valverde Villalba, Rafael Carrasco Ruiz, Juan Moral Fernandez.



