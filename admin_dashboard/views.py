from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def admin_dashboard(request):
    return render(request,'admin_dashboard/admin_base.html')


def demo_form(request):
    return render(request,'admin_dashboard/forms-advanced-form.html')