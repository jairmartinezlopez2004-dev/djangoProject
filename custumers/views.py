from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Paciente, Cita, Consulta
import datetime


# ==================== VISTAS DE PACIENTES ====================

@login_required
@permission_required('custumers.view_paciente', raise_exception=True)
def paciente_list(request):
    """
    Lista de pacientes - Solo accesible por Admin y Recepcionista
    """
    pacientes = Paciente.objects.all()
    return render(request, 'custumers/paciente_list.html', {'pacientes': pacientes})


@login_required
@permission_required('custumers.add_paciente', raise_exception=True)
def paciente_create(request):
    """
    Crear nuevo paciente - Solo accesible por Admin y Recepcionista
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre_completo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        try:
            from django.contrib.auth.models import User
            # Crear usuario asociado
            username = nombre.lower().replace(' ', '')
            user = User.objects.create_user(
                username=username,
                email=f'{username}@temp.com',
                password='temp123'
            )
            
            paciente = Paciente.objects.create(
                usuario=user,
                nombre_completo=nombre,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, 'Paciente creado exitosamente')
            return redirect('paciente_list')
        except Exception as e:
            messages.error(request, f'Error al crear paciente: {e}')
    
    return render(request, 'custumers/paciente_form.html')


@login_required
@permission_required('custumers.view_paciente', raise_exception=True)
def paciente_detail(request, pk):
    """
    Ver detalles de paciente - Solo accesible por Admin, Recepcionista y Doctor
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'custumers/paciente_detail.html', {'paciente': paciente})


# ==================== VISTAS DE CITAS ====================

@login_required
@permission_required('custumers.view_cita', raise_exception=True)
def cita_list(request):
    """
    Lista de citas - Accesible por Admin, Recepcionista, Doctor y Paciente
    Los pacientes solo ven sus propias citas
    """
    if request.user.groups.filter(name='Paciente').exists():
        # Paciente solo ve sus propias citas
        try:
            paciente = request.user.paciente
            citas = Cita.objects.filter(paciente=paciente)
        except Paciente.DoesNotExist:
            citas = []
    else:
        # Otros roles ven todas las citas
        citas = Cita.objects.all()
    
    return render(request, 'custumers/cita_list.html', {'citas': citas})


@login_required
@permission_required('custumers.add_cita', raise_exception=True)
def cita_create(request):
    """
    Crear nueva cita - Solo accesible por Admin y Recepcionista
    """
    if request.method == 'POST':
        try:
            paciente = Paciente.objects.get(pk=request.POST.get('paciente'))
            doctor_id = request.POST.get('doctor')
            fecha = request.POST.get('fecha')
            motivo = request.POST.get('motivo')
            
            from django.contrib.auth.models import User
            doctor = User.objects.get(pk=doctor_id) if doctor_id else None
            
            Cita.objects.create(
                paciente=paciente,
                doctor=doctor,
                fecha=fecha,
                motivo=motivo
            )
            messages.success(request, 'Cita creada exitosamente')
            return redirect('cita_list')
        except Exception as e:
            messages.error(request, f'Error al crear cita: {e}')
    
    pacientes = Paciente.objects.all()
    from django.contrib.auth.models import User
    doctores = User.objects.filter(groups__name='Doctor')
    
    return render(request, 'custumers/cita_form.html', {
        'pacientes': pacientes,
        'doctores': doctores
    })


@login_required
@permission_required('custumers.change_cita', raise_exception=True)
def cita_update(request, pk):
    """
    Actualizar cita - Solo accesible por Admin y Recepcionista
    """
    cita = get_object_or_404(Cita, pk=pk)
    
    if request.method == 'POST':
        cita.estado = request.POST.get('estado')
        cita.notas = request.POST.get('notas')
        cita.save()
        messages.success(request, 'Cita actualizada exitosamente')
        return redirect('cita_list')
    
    return render(request, 'custumers/cita_update.html', {'cita': cita})


@login_required
@permission_required('custumers.delete_cita', raise_exception=True)
def cita_delete(request, pk):
    """
    Eliminar cita - Solo accesible por Admin y Recepcionista
    """
    cita = get_object_or_404(Cita, pk=pk)
    
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada exitosamente')
        return redirect('cita_list')
    
    return render(request, 'custumers/cita_confirm_delete.html', {'cita': cita})


# ==================== VISTAS DE CONSULTAS ====================

@login_required
@permission_required('custumers.view_consulta', raise_exception=True)
def consulta_list(request):
    """
    Lista de consultas - Accesible por Admin, Doctor y Paciente
    Los pacientes solo ven sus propias consultas
    """
    if request.user.groups.filter(name='Paciente').exists():
        # Paciente solo ve sus propias consultas
        try:
            paciente = request.user.paciente
            consultas = Consulta.objects.filter(paciente=paciente)
        except Paciente.DoesNotExist:
            consultas = []
    else:
        # Otros roles ven todas las consultas
        consultas = Consulta.objects.all()
    
    return render(request, 'custumers/consulta_list.html', {'consultas': consultas})


@login_required
@permission_required('custumers.add_consulta', raise_exception=True)
def consulta_create(request, cita_pk=None):
    """
    Crear nueva consulta - Solo accesible por Admin y Doctor
    """
    if request.method == 'POST':
        try:
            paciente = Paciente.objects.get(pk=request.POST.get('paciente'))
            diagnostico = request.POST.get('diagnostico')
            tratamiento = request.POST.get('tratamiento')
            receta = request.POST.get('receta', '')
            observaciones = request.POST.get('observaciones', '')
            
            cita = None
            if cita_pk:
                cita = Cita.objects.get(pk=cita_pk)
            
            Consulta.objects.create(
                paciente=paciente,
                doctor=request.user,
                cita=cita,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                receta=receta,
                observaciones=observaciones
            )
            messages.success(request, 'Consulta creada exitosamente')
            return redirect('consulta_list')
        except Exception as e:
            messages.error(request, f'Error al crear consulta: {e}')
    
    pacientes = Paciente.objects.all()
    cita = None
    if cita_pk:
        cita = Cita.objects.get(pk=cita_pk)
    
    return render(request, 'custumers/consulta_form.html', {
        'pacientes': pacientes,
        'cita': cita
    })


@login_required
@permission_required('custumers.change_consulta', raise_exception=True)
def consulta_detail(request, pk):
    """
    Ver detalles de consulta - Solo accesible por Admin y Doctor
    """
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'custumers/consulta_detail.html', {'consulta': consulta})


# ==================== VISTA DE DASHBOARD ====================

@login_required
def dashboard(request):
    """
    Dashboard principal - Accesible por todos los usuarios autenticados
    Muestra diferente contenido según el rol del usuario
    """
    context = {
        'user_groups': request.user.groups.all(),
        'is_admin': request.user.groups.filter(name='Administrador').exists(),
        'is_recepcionista': request.user.groups.filter(name='Recepcionista').exists(),
        'is_doctor': request.user.groups.filter(name='Doctor').exists(),
        'is_paciente': request.user.groups.filter(name='Paciente').exists(),
    }
    
    # Agregar datos específicos según el rol
    if context['is_admin']:
        context['total_pacientes'] = Paciente.objects.count()
        context['total_citas'] = Cita.objects.count()
        context['total_consultas'] = Consulta.objects.count()
    
    elif context['is_recepcionista']:
        context['citas_hoy'] = Cita.objects.filter(fecha__date__gte=datetime.date.today()).count()
        context['citas_pendientes'] = Cita.objects.filter(estado='programada').count()
    
    elif context['is_doctor']:
        context['mis_citas'] = Cita.objects.filter(doctor=request.user).count()
        context['mis_consultas'] = Consulta.objects.filter(doctor=request.user).count()
    
    elif context['is_paciente']:
        try:
            paciente = request.user.paciente
            context['mis_citas'] = Cita.objects.filter(paciente=paciente).count()
            context['mis_consultas'] = Consulta.objects.filter(paciente=paciente).count()
        except Paciente.DoesNotExist:
            context['mis_citas'] = 0
            context['mis_consultas'] = 0
    
    return render(request, 'custumers/dashboard.html', context)
