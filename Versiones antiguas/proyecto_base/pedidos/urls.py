from django.conf.urls import patterns, url

from pedidos import views

urlpatterns = patterns ('',
	url(r'^$',views.index, name='index'),
	url(r'^alta_usuario/',views.alta_usuario, name='alta_usuario'),
	url(r'^asignar_pedido/',views.asignar_pedido, name='asignar_pedido'),
	url(r'^actualizar_pedido/',views.actualizar_pedido, name='actualizar_pedido'),
	url(r'^estado_pedido/',views.estado_pedido, name='estado_pedido'),
)
