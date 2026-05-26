from django.db import models
from django.contrib.auth.models import User


class Paciente(models.Model):
    """
    Modelo de Paciente para el sistema médico.
    Genera permisos automáticos: add_paciente, view_paciente, change_paciente, delete_paciente
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente')
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    seguro_medico = models.CharField(max_length=100, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-creado']

    def __str__(self):
        return self.nombre_completo


class Cita(models.Model):
    """
    Modelo de Cita médica.
    Genera permisos automáticos: add_cita, view_cita, change_cita, delete_cita
    """
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='citas_asignadas')
    fecha = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    notas = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha']

    def __str__(self):
        return f"Cita de {self.paciente.nombre_completo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class Consulta(models.Model):
    """
    Modelo de Consulta médica (historial).
    Genera permisos automáticos: add_consulta, view_consulta, change_consulta, delete_consulta
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='consultas_realizadas')
    cita = models.OneToOneField(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name='consulta')
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    receta = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Consulta de {self.paciente.nombre_completo} - {self.fecha.strftime('%Y-%m-%d')}"
