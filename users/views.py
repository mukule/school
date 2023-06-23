from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

class login(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/index.html'
