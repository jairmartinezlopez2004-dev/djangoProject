from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from custumers.models import Paciente, Cita, Consulta
from users.models import Product


class Command(BaseCommand):
    help = 'Crea los grupos (roles) y asigna permisos iniciales para el sistema médico'

    def handle(self, *args, **options):
        # Obtener ContentTypes de los modelos
        ct_paciente = ContentType.objects.get_for_model(Paciente)
        ct_cita = ContentType.objects.get_for_model(Cita)
        ct_consulta = ContentType.objects.get_for_model(Consulta)
        ct_product = ContentType.objects.get_for_model(Product)

        # --- GRUPO: ADMINISTRADOR ---
        # Tiene TODOS los permisos del sistema
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        if created:
            # Asignar todos los permisos de las apps relevantes
            all_permissions = Permission.objects.filter(
                content_type__app_label__in=['custumers', 'users']
            )
            admin_group.permissions.set(all_permissions)
            self.stdout.write(self.style.SUCCESS('Grupo "Administrador" creado con todos los permisos'))
        else:
            self.stdout.write(self.style.WARNING('Grupo "Administrador" ya existe'))

        # --- GRUPO: RECEPCIONISTA ---
        # Puede gestionar citas y ver pacientes
        recepcionista_group, created = Group.objects.get_or_create(name='Recepcionista')
        if created:
            recepcionista_permissions = [
                # Permisos de Paciente (solo ver y crear)
                Permission.objects.get(codename='view_paciente', content_type=ct_paciente),
                Permission.objects.get(codename='add_paciente', content_type=ct_paciente),
                Permission.objects.get(codename='change_paciente', content_type=ct_paciente),
                # Permisos de Cita (CRUD completo)
                Permission.objects.get(codename='view_cita', content_type=ct_cita),
                Permission.objects.get(codename='add_cita', content_type=ct_cita),
                Permission.objects.get(codename='change_cita', content_type=ct_cita),
                Permission.objects.get(codename='delete_cita', content_type=ct_cita),
                # Permisos de Consulta (solo ver)
                Permission.objects.get(codename='view_consulta', content_type=ct_consulta),
            ]
            recepcionista_group.permissions.set(recepcionista_permissions)
            self.stdout.write(self.style.SUCCESS('Grupo "Recepcionista" creado'))
        else:
            self.stdout.write(self.style.WARNING('Grupo "Recepcionista" ya existe'))

        # --- GRUPO: DOCTOR ---
        # Puede ver pacientes, gestionar consultas, ver citas
        doctor_group, created = Group.objects.get_or_create(name='Doctor')
        if created:
            doctor_permissions = [
                # Permisos de Paciente (solo ver)
                Permission.objects.get(codename='view_paciente', content_type=ct_paciente),
                # Permisos de Cita (solo ver y cambiar estado)
                Permission.objects.get(codename='view_cita', content_type=ct_cita),
                Permission.objects.get(codename='change_cita', content_type=ct_cita),
                # Permisos de Consulta (CRUD completo)
                Permission.objects.get(codename='view_consulta', content_type=ct_consulta),
                Permission.objects.get(codename='add_consulta', content_type=ct_consulta),
                Permission.objects.get(codename='change_consulta', content_type=ct_consulta),
                Permission.objects.get(codename='delete_consulta', content_type=ct_consulta),
            ]
            doctor_group.permissions.set(doctor_permissions)
            self.stdout.write(self.style.SUCCESS('Grupo "Doctor" creado'))
        else:
            self.stdout.write(self.style.WARNING('Grupo "Doctor" ya existe'))

        # --- GRUPO: PACIENTE ---
        # Solo puede ver sus propias citas y consultas (se maneja en vistas)
        paciente_group, created = Group.objects.get_or_create(name='Paciente')
        if created:
            paciente_permissions = [
                # Permisos mínimos para ver información
                Permission.objects.get(codename='view_cita', content_type=ct_cita),
                Permission.objects.get(codename='view_consulta', content_type=ct_consulta),
            ]
            paciente_group.permissions.set(paciente_permissions)
            self.stdout.write(self.style.SUCCESS('Grupo "Paciente" creado'))
        else:
            self.stdout.write(self.style.WARNING('Grupo "Paciente" ya existe'))

        # --- RESUMEN DE PERMISOS POR ROL ---
        self.stdout.write('\n' + '='*50)
        self.stdout.write('RESUMEN DE PERMISOS POR ROL:')
        self.stdout.write('='*50)
        
        for group in [admin_group, recepcionista_group, doctor_group, paciente_group]:
            self.stdout.write(f'\n📋 {group.name}:')
            for perm in group.permissions.all():
                self.stdout.write(f'   - {perm.content_type.app_label}.{perm.codename}')

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✓ Grupos y permisos configurados correctamente'))
        self.stdout.write('='*50)
