from django.conf.urls import patterns, url

from pedidos import views

urlpatterns = patterns ('',
	url(r'^$',views.index, name='index'),
	url(r'^alta_usuario/',views.alta_usuario, name='alta_usuario'),
	url(r'^asignar_pedido/',views.asignar_pedido, name='asignar_pedido'),
	url(r'^actualizar_pedido/',views.actualizar_pedido, name='actualizar_pedido'),
	url(r'^estado_pedido/',views.estado_pedido, name='estado_pedido'),
	url(r'^administrar/',views.administrar, name='administrar'),
	url(r'^admin_estados/',views.admin_estados, name='admin_estados'),
	url(r'^cerrar_sesion/',views.cerrar_sesion, name='cerrar_sesion'),
)


