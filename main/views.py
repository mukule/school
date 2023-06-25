from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'main/dashboard.html')

def dashboard_admin(request):
    return render(request, 'adminstrator/dashboard.html')

