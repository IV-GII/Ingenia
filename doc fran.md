Puesta a punto de Ingenia Tracking
==================================

Después de pensar detenidamente en que lenguaje trabajar, preguntándonos los pros y contras de cada uno nos decantamos por python, concretamente en el framework django por varios motivos:
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

Chef
====


Alta de usuario
===============
Esta vista solo se podrá acceder su eres un trabajador de la empresa. Una vez que el cliente solicita el seguimiento de su pedido, uno de los trabajadores de la empresa Ingenia le dará de alta en el sistema, facilitándole un usuario y una contraseña de acceso.<br><br>
Esta es la apariencia que cuenta el alta de usuario:

![captura_alta](https://dl.dropbox.com/s/6dqdhta5crp1wgf/alta_user.png)

Como se puede apreciar se trata de un simple formulario que una vez que sea valido sus entradas se añadirá una nueva fila a la tabla de usuarios.

Para poder mostrar un formulario en django se debe generar una clase especifica en el archivo forms.py de la carpeta de nuestra aplicación. En este caso como vamos a usar todos los campos de la tabla podemos hacerlo tal que así:
~~~~~~{.python}
class UsuariosForm(forms.ModelForm):
	class Meta:
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
	class Meta:
		model = Pedidos
~~~~~~






