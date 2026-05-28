from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Confirmacion(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    asistira = models.BooleanField(default=True, verbose_name="¿Asistirá?")
    numero_adultos = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name="Número de adultos"
    )
    numero_ninos = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name="Número de niños"
    )
    mensaje = models.TextField(blank=True, verbose_name="Mensaje (opcional)")
    comprobante = models.FileField(upload_to='comprobantes/', blank=True, null=True, verbose_name="Comprobante de transferencia")
    # Restricciones alimentarias
    celiaco = models.BooleanField(default=False, verbose_name="Celíaco/a")
    celiaco_cantidad = models.IntegerField(default=0, verbose_name="Cantidad celíacos")
    vegano = models.BooleanField(default=False, verbose_name="Vegano/a")
    vegano_cantidad = models.IntegerField(default=0, verbose_name="Cantidad veganos")
    vegetariano = models.BooleanField(default=False, verbose_name="Vegetariano/a")
    vegetariano_cantidad = models.IntegerField(default=0, verbose_name="Cantidad vegetarianos")
    restriccion_otro = models.BooleanField(default=False, verbose_name="Otra restricción")
    restriccion_otro_detalle = models.CharField(max_length=300, blank=True, verbose_name="Detalle otra restricción")
    # Preferencia de bebida
    bebida = models.CharField(max_length=50, blank=True, verbose_name="Bebida preferida")
    fecha_confirmacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de confirmación")
    
    class Meta:
        verbose_name = "Confirmación"
        verbose_name_plural = "Confirmaciones"
        ordering = ['-fecha_confirmacion']
    
    def __str__(self):
        return f"{self.nombre} - {'Asiste' if self.asistira else 'No asiste'} ({self.numero_personas} persona{'s' if self.numero_personas > 1 else ''})"
