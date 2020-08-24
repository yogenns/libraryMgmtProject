from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import forms
app_name = 'library_app'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url('login/', auth_views.LoginView.as_view(template_name='library_app/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url('signup/', views.SignUp.as_view(), name='signup'),
    url('genre/', views.CreateGenreView.as_view(), name='genre'),
    url('author/', views.CreateAuthorView.as_view(), name='author'),
    url('upload_book/',  views.ContactWizard.as_view(
        [forms.UploadBookForm1, forms.SelectAuthorForm2]), name='upload_book'),
    url('books/', views.BookListView.as_view(), name='books'),
    url('view/book/(?P<pk>\d+)/', views.BookDetailView.as_view(), name='book_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
