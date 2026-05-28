from django.contrib import admin
from django.utils.html import format_html
from .models import Confirmacion

# Register your models here.

@admin.register(Confirmacion)
class ConfirmacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asistira', 'numero_adultos', 'numero_ninos', 'bebida', 'ver_comprobante', 'fecha_confirmacion')
    list_filter = ('asistira', 'fecha_confirmacion')
    search_fields = ('nombre', 'email')
    readonly_fields = ('fecha_confirmacion', 'ver_comprobante')

    def ver_comprobante(self, obj):
        if obj.comprobante:
            return format_html('<a href="{}" target="_blank">Ver comprobante</a>', obj.comprobante.url)
        return '—'
    ver_comprobante.short_description = 'Comprobante'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('fecha_confirmacion',)
        return self.readonly_fields
