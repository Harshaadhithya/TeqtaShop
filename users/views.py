from django.shortcuts import render

# Create your views here.

def user_login(request):
   
    context={'page_title':'login_page'}
    return render(request,'users/login.html',context)
