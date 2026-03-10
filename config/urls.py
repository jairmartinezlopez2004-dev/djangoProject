from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import get_user, inicio, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/', get_user, name='cliente'),
    path('inicio/', inicio, name='inicio'),
    # LOGIN y LOGOUT
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/', http_method_names=['get', 'post']), name='logout'),
    # REGISTRO
    path('register/', register, name='register'),
]




