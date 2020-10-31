import json

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from user_access.forms import LoginForm, RegisterForm


class LoginView(TemplateView):
    """
    View for login into the application
    """
    template_name = 'login.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        try:
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse('book_inventory_management:book_management'))
            else:
                context = {
                    'form': login_form
                }
                return render(request, 'login.html', context)
        except:
            context = {
                'form': login_form
            }
            return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_form = LoginForm(request.POST)
        print(login_form.is_valid(), "dasdasdas")
        if login_form.is_valid():
            user = authenticate(request, email=email, password=password)
            print(user,"sssssssssssss")
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('book_inventory_management:book_list'))
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context)


class RegisterUserView(TemplateView):
    """
    View for register into the application
    """
    template_name = 'register.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(RegisterUserView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        context = {
            'form': register_form
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        response_data ={'status':True}
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_obj = register_form.save()
            if request.POST.get('password'):
                user_obj.set_password(request.POST.get('password'))
                user_obj.save()
        else:
            response_data['status'] = False
            response_data['errors'] = register_form.errors
        return HttpResponse(json.dumps(response_data), content_type="application/json")