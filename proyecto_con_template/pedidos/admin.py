from django.contrib import admin
from pedidos.models import Usuarios, Pedidos

class linea_pedidos (admin.StackedInline):
    model = Pedidos
    extra = 1

class UsuariosAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['nombre']}),
        (None,               {'fields': ['correo_electronico']}),
	(None,		     {'fields': ['rol']}),
	(None,		     {'fields': ['password']}),
    ]
    inlines = [linea_pedidos]
    list_display = ('nombre', 'correo_electronico','rol','password')
    list_filter = ['nombre']
    search_fields = ['nombre']

admin.site.register(Usuarios, UsuariosAdmin)
