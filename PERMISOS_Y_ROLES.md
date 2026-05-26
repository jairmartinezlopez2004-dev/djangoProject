# Sistema de Permisos y Roles - Documentación

## 📋 Resumen del Sistema Implementado

Se ha implementado un sistema completo de permisos y roles basado en el sistema nativo de Django (Groups y Permissions) para un sistema médico.

## 🎯 Roles Implementados

### 1. **Administrador**
- **Permisos**: TODOS los permisos del sistema
- **Acceso**: Gestión completa de pacientes, citas, consultas y productos
- **Permisos específicos**:
  - `custumers.*` (todos los permisos de la app custumers)
  - `users.*` (todos los permisos de la app users)

### 2. **Recepcionista**
- **Permisos**: Gestión de citas y pacientes
- **Acceso**: 
  - Ver, crear y editar pacientes
  - Ver, crear, editar y eliminar citas
  - Ver consultas (solo lectura)
- **Permisos específicos**:
  - `custumers.view_paciente`
  - `custumers.add_paciente`
  - `custumers.change_paciente`
  - `custumers.view_cita`
  - `custumers.add_cita`
  - `custumers.change_cita`
  - `custumers.delete_cita`
  - `custumers.view_consulta`

### 3. **Doctor**
- **Permisos**: Gestión de consultas y visualización de información
- **Acceso**:
  - Ver pacientes (solo lectura)
  - Ver y cambiar estado de citas
  - Ver, crear, editar y eliminar consultas
- **Permisos específicos**:
  - `custumers.view_paciente`
  - `custumers.view_cita`
  - `custumers.change_cita`
  - `custumers.view_consulta`
  - `custumers.add_consulta`
  - `custumers.change_consulta`
  - `custumers.delete_consulta`

### 4. **Paciente**
- **Permisos**: Solo visualización de su propia información
- **Acceso**:
  - Ver sus propias citas
  - Ver sus propias consultas
- **Permisos específicos**:
  - `custumers.view_cita`
  - `custumers.view_consulta`

## 🗂️ Modelos Creados

### Paciente
- Relación One-to-One con User
- Campos: nombre_completo, telefono, direccion, fecha_nacimiento, seguro_medico
- Genera permisos: add_paciente, view_paciente, change_paciente, delete_paciente

### Cita
- Relación ForeignKey con Paciente y User (doctor)
- Campos: fecha, motivo, estado, notas
- Estados: programada, confirmada, completada, cancelada
- Genera permisos: add_cita, view_cita, change_cita, delete_cita

### Consulta
- Relación ForeignKey con Paciente y User (doctor)
- Relación One-to-One con Cita
- Campos: diagnostico, tratamiento, receta, observaciones
- Genera permisos: add_consulta, view_consulta, change_consulta, delete_consulta

## 🔧 Configuración Realizada

### 1. Settings (`config/settings.py`)
```python
INSTALLED_APPS = [
    # ... otras apps
    'custumers'  # App del sistema médico
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/inicio/'
LOGOUT_REDIRECT_URL = '/login/'
```

### 2. URLs (`config/urls.py`)
```python
urlpatterns = [
    # ... otras URLs
    path('', include('custumers.urls')),  # URLs del sistema médico
]
```

### 3. Comando de Management
```bash
python manage.py setup_roles
```
Este comando crea los grupos y asigna los permisos automáticamente.

## 🚀 Cómo Usar el Sistema

### Paso 1: Configurar Roles
```bash
python manage.py setup_roles
```

### Paso 2: Crear Usuarios y Asignar Roles

**Desde el Admin de Django:**
1. Ve a `/admin/`
2. Crea un nuevo usuario
3. Ve a `/admin/auth/group/`
4. Asigna el usuario al grupo correspondiente (Administrador, Recepcionista, Doctor, Paciente)

**Desde el Shell de Django:**
```python
from django.contrib.auth.models import User, Group

# Crear usuario
user = User.objects.create_user('doctor1', 'doctor1@email.com', 'password123')

# Asignar al grupo Doctor
doctor_group = Group.objects.get(name='Doctor')
user.groups.add(doctor_group)
```

### Paso 3: Probar los Permisos

1. **Login** con diferentes usuarios según su rol
2. **Navegar** por el sistema - el menú se mostrará según permisos
3. **Intentar acceder** a URLs sin permisos - verás la página 403

## 📡 URLs Disponibles

### Dashboard
- `/dashboard/` - Dashboard principal (requiere login)

### Pacientes
- `/pacientes/` - Lista de pacientes (view_paciente)
- `/pacientes/crear/` - Crear paciente (add_paciente)
- `/pacientes/<id>/` - Ver detalle paciente (view_paciente)

### Citas
- `/citas/` - Lista de citas (view_cita)
- `/citas/crear/` - Crear cita (add_cita)
- `/citas/<id>/editar/` - Editar cita (change_cita)
- `/citas/<id>/eliminar/` - Eliminar cita (delete_cita)

### Consultas
- `/consultas/` - Lista de consultas (view_consulta)
- `/consultas/crear/` - Crear consulta (add_consulta)
- `/consultas/<id>/` - Ver detalle consulta (change_consulta)

## 🛡️ Decoradores Utilizados

### Para vistas basadas en funciones (FBV)
```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('custumers.view_paciente', raise_exception=True)
def paciente_list(request):
    # ...
```

### Para vistas basadas en clases (CBV)
```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PacienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'custumers.view_paciente'
    raise_exception = True
    # ...
```

## 🎨 Verificación de Permisos en Templates

```html
{% if perms.custumers.view_paciente %}
    <a href="{% url 'paciente_list' %}">Ver Pacientes</a>
{% endif %}

{% if perms.custumers.add_cita %}
    <a href="{% url 'cita_create' %}">Nueva Cita</a>
{% endif %}
```

## 🔒 Página 403 Personalizada

Se ha creado una página de acceso denegado en `templates/403.html` que:
- Muestra el error de acceso denegado
- Indica el rol actual del usuario
- Proporciona enlaces para volver al dashboard o cerrar sesión

## 📊 Ejemplos de Uso

### Ejemplo 1: Verificar si un usuario tiene un permiso específico
```python
from django.contrib.auth.decorators import permission_required

@permission_required('custumers.add_cita', raise_exception=True)
def crear_cita(request):
    # Solo usuarios con permiso add_cita pueden acceder
    pass
```

### Ejemplo 2: Filtrar datos según el rol
```python
@login_required
def cita_list(request):
    if request.user.groups.filter(name='Paciente').exists():
        # Paciente solo ve sus propias citas
        citas = Cita.objects.filter(paciente=request.user.paciente)
    else:
        # Otros roles ven todas las citas
        citas = Cita.objects.all()
    return render(request, 'custumers/cita_list.html', {'citas': citas})
```

### Ejemplo 3: Verificar permisos en templates
```html
{% if perms.custumers.delete_cita %}
    <a href="{% url 'cita_delete' cita.pk %}">Eliminar</a>
{% endif %}
```

## 🔧 Mantenimiento

### Reconfigurar Roles
Si necesitas cambiar los permisos de un rol:
1. Ve a `/admin/auth/group/`
2. Edita el grupo correspondiente
3. Agrega o quita permisos según necesites

### Crear Nuevos Roles
1. Crea un nuevo comando de management o modifica `setup_roles.py`
2. Ejecuta `python manage.py setup_roles`
3. Asigna usuarios al nuevo grupo

## ✅ Verificación del Sistema

Para verificar que el sistema funciona correctamente:

1. **Crear usuarios de prueba** para cada rol
2. **Login con cada usuario** y verificar:
   - El menú muestra las opciones correctas
   - Puede acceder a las URLs permitidas
   - Recibe error 403 al intentar acceder a URLs prohibidas
3. **Probar el flujo completo** de creación de citas y consultas

## 📝 Notas Importantes

- El sistema usa `raise_exception=True` en los decoradores para mostrar el error 403 en lugar de redirigir al login
- Los pacientes solo pueden ver sus propias citas y consultas (filtrado en las vistas)
- El comando `setup_roles` puede ejecutarse múltiples veces sin problemas
- Todos los permisos se basan en el sistema nativo de Django

## 🎓 Referencias

Basado en el tutorial de permisos de Django:
https://github.com/lrioscoutino/curso-python/tree/main/django_permissions

Documentación oficial de Django:
https://docs.djangoproject.com/en/6.0/topics/auth/default/#permissions
