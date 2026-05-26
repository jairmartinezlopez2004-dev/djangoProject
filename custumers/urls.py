from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # URLs de Pacientes
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/crear/', views.paciente_create, name='paciente_create'),
    path('pacientes/<int:pk>/', views.paciente_detail, name='paciente_detail'),
    
    # URLs de Citas
    path('citas/', views.cita_list, name='cita_list'),
    path('citas/crear/', views.cita_create, name='cita_create'),
    path('citas/<int:pk>/editar/', views.cita_update, name='cita_update'),
    path('citas/<int:pk>/eliminar/', views.cita_delete, name='cita_delete'),
    
    # URLs de Consultas
    path('consultas/', views.consulta_list, name='consulta_list'),
    path('consultas/crear/', views.consulta_create, name='consulta_create'),
    path('consultas/crear/<int:cita_pk>/', views.consulta_create, name='consulta_create_from_cita'),
    path('consultas/<int:pk>/', views.consulta_detail, name='consulta_detail'),
]
