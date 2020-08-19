from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


class HomeView(TemplateView):
    template_name = 'library_app/home.html'


class SignUp(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('library_app:login')
    template_name = 'library_app/signup.html'


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class CreateGenreView(SuperUserRequiredMixin, CreateView):
    form_class = forms.CreateGenreForm
    success_url = reverse_lazy('library_app:genre')
    template_name = 'library_app/genre.html'

    def get_context_data(self, **kwargs):
        kwargs['genre_list'] = models.Genre.objects.order_by('id')
        return super(CreateGenreView, self).get_context_data(**kwargs)
