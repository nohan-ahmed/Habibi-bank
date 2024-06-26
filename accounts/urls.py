from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('profile/', views.UserBankAccountUpdateView.as_view(), name='profile'),
    path('profile/password-change/', PasswordChangeView.as_view(template_name='./accounts/password_change_form.html', success_url=reverse_lazy('profile')), name='password_change'),

]
