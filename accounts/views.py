from django.shortcuts import render,redirect
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from .forms import RegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class UserRegistrationView(FormView):
    template_name = './accounts/register.html'
    form_class = RegistrationForm
    success_url= reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user=user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = './accounts/login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('profile')

@login_required
def UserLogout(request):
    logout(request)
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})