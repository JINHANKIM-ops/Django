from blog.models import Post, PostComment
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
import mimetypes
import urllib
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(req):
    post_list = Post.objects.all().order_by('-createDate')

    paginator = Paginator(post_list, 6)
    page = req.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "post_latest": post_list,
        "page": page,
        "posts": posts
    }

    return render(req, 'index.html', context)


def login(req):
    if req.method == "post":
        username = req.post['username']
        password = req.post['password']
        user = auth.authenticate(req, username=username, password=password)
        if user is not None:
            auth.login(req, user)
            return redirect('index')
        else:
            return render(req, 'blog/login_form.html', {'error': 'username or password is incorrect'})
    else:
        return render(req, 'blog/login_form.html')


def logout(req):
    auth.logout(req)
    return redirect('index')


def signup(req):
    if req.method == "POST":
        if req.POST["password"] == req.POST["password"]:
            user = User.objects.create_user(username=req.POST["username"], password=req.POST["password"])
            auth.login(req, user)
            return redirect('index')
        return render(req, 'blog/signup_form.html')
    return render(req, 'blog/signup_form.html')


def conn_write(req, post_pk):
    if req.method == "POST":
        conn_user = req.user
        conn_content = req.POST['content']
        post = get_object_or_404(Post, pk=post_pk)
        conn_profile = User.objects.get(username=conn_user)

        PostComment.objects.create(board=post, writer=conn_profile, text=conn_content)

        if not conn_content:
            return HttpResponseRedirect(reverse_lazy('blog/post_detail.html', post_pk))

        return HttpResponseRedirect(reverse_lazy('index'))


class CommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def conn_update(req, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    board = get_object_or_404(Post, pk=comment.board.id)

    if req.user != comment.writer:
        return redirect(board)

    if req.method == "POST":
        form = CommentForm(req.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(board)
    else:
        form = CommentForm(instance=comment)
    return render(req, 'blog/conn_update.html', {'form': form})


def conn_delete(req, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    board = get_object_or_404(Post, pk=comment.board.id)

    if req.user != comment.writer and not req.user.is_staff:
        return redirect(board)

    if req.method == "POST":
        comment.delete()
        return redirect(board)
    else:
        return render(req, 'blog/conn_delete.html', {'object': comment})


def file_download_view(request, pk):
    notice = get_object_or_404(Post, pk=pk)
    url = notice.title_image.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(notice.title_image.url)
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "title_image", "content", "category"]
    success_url = '/'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "title_image", "content", "category"]
    context_object_name = 'post'
    template_name = 'blog/update_form.html'
    success_url = '/'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    fields = ["title"]
    context_object_name = 'remove'
    success_url = '/'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post




