from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from . import forms
# Create your views here.


class HomeView(TemplateView):
    template_name = 'library_app/home.html'


class SignUp(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('library_app:login')
    template_name = 'library_app/signup.html'
