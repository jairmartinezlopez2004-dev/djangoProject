from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from users.views import get_user, inicio, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/', get_user, name='cliente'),
    path('inicio/', inicio, name='inicio'),
    # LOGIN y LOGOUT
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/', http_method_names=['get', 'post']), name='logout'),
    # REGISTRO
    path('register/', register, name='register'),
    # PASSWORD RESET
    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    # URLs del módulo custumers (sistema médico)
    path('', include('custumers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




