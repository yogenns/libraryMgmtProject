from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
import zipfile
from lxml import etree
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from PyPDF2 import PdfFileReader
# Create your views here.


class HomeView(TemplateView):
    template_name = 'library_app/home.html'

    def get_context_data(self, **kwargs):
        kwargs['recommended_list'] = list(models.RecommendedBook.objects.order_by(
            'id'))
        return super(HomeView, self).get_context_data(**kwargs)


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


class CreateAuthorView(SuperUserRequiredMixin, CreateView):
    form_class = forms.CreateAuthorForm
    success_url = reverse_lazy('library_app:author')
    template_name = 'library_app/author.html'

    def get_context_data(self, **kwargs):
        kwargs['author_list'] = models.Author.objects.order_by('id')
        return super(CreateAuthorView, self).get_context_data(**kwargs)


class BookListView(ListView):
    paginate_by = 10
    model = models.Book

    def get_queryset(self):
        return models.Book.objects.all().order_by('pk')

    def post(self, request, *args, **kwargs):
        # print(request.POST.get("selectedRows"))
        row_list = request.POST.get("selectedRows").split(',')
        for row in row_list:
            print("Delete Book with Id "+row)
            try:
                remove_book = models.Book.objects.get(pk=row)
                # Remove Cover
                if os.path.exists(remove_book.book_cover.path):
                    print("Removed file "+remove_book.book_cover.path)
                    os.remove(remove_book.book_cover.path)
                else:
                    print("The file does not exist " +
                          remove_book.book_cover.path)
                # Remove File
                if remove_book.book_file != '':
                    if os.path.exists(remove_book.book_file.path):
                        print("Removed file "+remove_book.book_file.path)
                        os.remove(remove_book.book_file.path)
                    else:
                        print("The file does not exist " +
                              remove_book.book_file.path)
                remove_book.delete()
            except models.Book.DoesNotExist:
                print("Cannot Remove Book. Object Does not exit")

        return self.get(request, *args, **kwargs)


class ContactWizard(SuperUserRequiredMixin, SessionWizardView):
    template_name = 'library_app/upload_book.html'
    success_url = reverse_lazy('library_app:books')
    tmp_file_location = 'tmp_files'
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, tmp_file_location))
    file_path = ""
    title = ""
    publisher = ""
    year = ""
    description = ""

    def process_step(self, form):
        if self.steps.current == '0':
            self.file_path = os.path.join(
                settings.MEDIA_ROOT, self.tmp_file_location, form.cleaned_data['book_file'].name)
            print(self.file_path)
        return self.get_form_step_data(form)

    def get_form_initial(self, step):
        initial_dict = self.initial_dict.get(step, {})
        print("Process Step "+step+" title "+self.title)
        if step == '1' and self.file_path != '':
            author = ""
            if self.file_path.endswith(".pdf"):
                pdf_info = extract_information(self.file_path)
                author = pdf_info['author']
                self.title = pdf_info['title']
                self.publisher = pdf_info['publisher']
            else:
                epub_info = get_epub_info(self.file_path)
                author = epub_info['creator']
                self.title = epub_info['title']
                self.publisher = epub_info['publisher']
                self.year = epub_info['date']
                self.description = epub_info['description']
            try:
                db_author = models.Author.objects.get(name=author)
            except models.Author.DoesNotExist:
                db_author = None
            print(db_author)
            if db_author != None:
                initial_dict = {'author': db_author.pk}

            initial_dict.update({'title': self.title, 'author_name': author, 'publication': self.publisher,
                                 'description': self.description, 'year': self.year, 'uploader': self.request.user.username})
        print(initial_dict)
        return initial_dict

    def done(self, form_list, **kwargs):
        book = models.Book()
        for form in form_list:
            if isinstance(form, forms.UploadBookForm1):
                print("UploadBookForm")
                book.book_file = form.cleaned_data['book_file']
            if isinstance(form, forms.SelectAuthorForm2):
                print("BasicValuesForm")
                author_name = form.cleaned_data['author_name']
                book.title = form.cleaned_data['title']
                book.genre = form.cleaned_data['genre']
                book.book_cover = form.cleaned_data['book_cover']
                book.description = form.cleaned_data['description']
                book.uploader = form.cleaned_data['uploader']
                book.publication = form.cleaned_data['publication']
                book.year = form.cleaned_data['year']

                try:
                    db_author = models.Author.objects.get(name=author_name)
                except models.Author.DoesNotExist:
                    db_author = None
                if db_author == None:
                    db_author = models.Author()
                    db_author.name = author_name
                    db_author.save()
                book.author = db_author
        book.save()

        return HttpResponseRedirect('/books/')


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
        Information about {pdf_path}:

        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {number_of_pages}
        """

    # print(txt)
    return {'author': information.author, 'title': information.title, 'total_pages': number_of_pages, 'publisher': information.producer}


def get_epub_info(fname):
    ns = {
        'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]
    # repackage the data
    res = {}
    for s in ['title', 'creator', 'publisher', 'date', 'description']:
        value_list = p.xpath('dc:%s/text()' % (s), namespaces=ns)
        if len(value_list) > 0:
            res[s] = value_list[0]
        else:
            res[s] = ''

    return res


class BookDetailView(DetailView):
    model = models.Book

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        try:
            user = self.request.user
            user_account = get_object_or_404(
                models.UserAccount, pk=user.pk)
            if user_account.borrowed_books.filter(pk=self.kwargs.get('pk')).count() > 0:
                kwargs['is_book_borrowed'] = True
        except:
            print("User Account Not Present")
        return super(BookDetailView, self).get_context_data(**kwargs)


class CreateRecommendedBookListView(SuperUserRequiredMixin, CreateView):
    model = models.RecommendedBook
    form_class = forms.CreateRecommendedBookForm
    success_url = reverse_lazy('library_app:recommended_books')
    template_name = 'library_app/recommendedbook_list.html'

    def get_context_data(self, **kwargs):
        kwargs['recommendedbook_list'] = models.RecommendedBook.objects.order_by(
            'pk')
        return super(CreateRecommendedBookListView, self).get_context_data(**kwargs)


class DeleteRecommendedBookView(SuperUserRequiredMixin, DeleteView):
    model = models.RecommendedBook
    success_url = reverse_lazy('library_app:recommended_books')

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_list = self.request.POST.get("selectedRows").split(',')
        if 'all' in selected_list:
            return queryset
        else:
            print(selected_list)
            return queryset.filter(pk__in=selected_list)

    def delete(self, *args, **kwargs):
        topics = self.get_queryset()
        print("Deleting RecommendedBook")
        print(topics)
        topics.delete()
        return HttpResponseRedirect('/recommended_books/')


@login_required
def borrow_book(request):
    if request.method == 'POST':
        borrow_id = request.POST['borrowBookId']
        book = get_object_or_404(models.Book, pk=borrow_id)
        user = request.user

        user_account = get_object_or_404(models.UserAccount, pk=user.pk)
        if user_account.borrowed_books.all().count() >= 2:
            return HttpResponseRedirect('/view/book/'+borrow_id+'/?limitcrossed=true')
        else:
            user_account.borrowed_books.add(book)
            return HttpResponseRedirect('/view/book/'+borrow_id)
    else:
        return Http404


@login_required
def return_book(request):
    if request.method == 'POST':
        returnBookId = request.POST['returnBookId']
        book = get_object_or_404(models.Book, pk=returnBookId)
        user = request.user

        user_account = get_object_or_404(models.UserAccount, pk=user.pk)
        user_account.borrowed_books.remove(book)
        return HttpResponseRedirect('/view/book/'+returnBookId)
    else:
        return Http404
