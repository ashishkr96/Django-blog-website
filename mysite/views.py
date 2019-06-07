from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment, About,Images
from .forms import UserUpdateForm, ProfileUpdateForm, Commentform, CreatePost, AboutMe
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import modelformset_factory


# Create your views here.

def about(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AboutMe(request.POST)
            if form.is_valid():
                about = form.cleaned_data['about']
                saving = About(user=request.user, about=about)
                saving.save()
                return HttpResponseRedirect(reverse('blog-home'))
        else:
            form = AboutMe()
            context = {
                'form': form
            }
            return render(request, 'mysite/about.html', context)


def newpasswordset(request):
    if request.user.has_usable_password():

        return redirect('password_change')


    else:
        if request.method == 'POST':
            print('false')
            form = SetPasswordForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, f'Password has been set sucessfully')
                return HttpResponseRedirect(reverse('blog-home'))
            else:
                messages.warning(request, f'Password is similar to username or is invalid')
                return redirect('password_new_set')
        else:
            form = SetPasswordForm(user=request.user)
            context = {
                'form': form,
            }
        return render(request, 'mysite/password-set-new.html', context)


def passchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'Password has been changed sucessfully')
            return HttpResponseRedirect(reverse('blog-home'))
        else:
            messages.warning(request, f'Password contains username or is invalid')
            return redirect('password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form,
        }
    return render(request, 'mysite/password_change.html', context)


def likes(request):
    post = get_object_or_404(Post, id=request.POST.get('like'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


@login_required()
def profile(request):
    if request.method == 'POST':
        updateform = UserUpdateForm(request.POST, instance=request.user)
        profileupdate = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if updateform.is_valid() and profileupdate.is_valid():
            updateform.save()
            profileupdate.save()
            return redirect('blog-home')
    else:
        updateform = UserUpdateForm()
        profileupdate = ProfileUpdateForm()
    context = {
        'title': 'Profile',
        'posts': Post.published.all(),
        'uform': updateform,
        'pform': profileupdate,
    }
    return render(request, 'mysite/profile.html', context)


def user_post(request, author):
    post = Post.published.filter(author_id=author)
    about = About.objects.filter(user=author).last()
    context = {
        'posts': post,
        'abouts': about,
    }
    return render(request, 'mysite/user_post.html', context)


def post_listview(request):
    post_list = Post.published.all().order_by('-id')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        post = Post.published.filter(
            Q(title__icontains=query) | Q(author__username=query) | Q(content__icontains=query))

    context = {
        'posts': post,

    }

    return render(request, 'mysite/index.html', context)


def post_draft(request):
    post_list = Post.draft.filter(author=request.user).order_by('-id')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        post = Post.published.filter(
            Q(title__icontains=query) | Q(author__username=query) | Q(content__icontains=query))

    context = {
        'posts': post,
    }
    return render(request, 'mysite/post_draft.html', context)


def delete_comment(request, id):
   if request.method == 'POST':
         pid = request.POST.get('pid')
         post = Post.object.get(id=pid)
         c = Comment.objects.filter(user=request.user, id=id).delete()

         return HttpResponseRedirect(post.get_absolute_url())


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

    if request.method == 'POST':
        form = Commentform(request.POST, post.pk)
        if form.is_valid():
            comment = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            a = Comment.objects.create(post=post, user=request.user, content=comment, reply=comment_qs)
            a.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = Commentform()
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comment': comments,
        'form': form,

    }
    return render(request, 'mysite/post_detail.html', context)


@login_required
def create_post(request):
    if request.user.is_superuser:
        ImageFormset = modelformset_factory(Images, fields=('pic',), extra=3)
        if request.method == 'POST':
            form = CreatePost(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                content = request.POST.get('content')
                title = request.POST.get('title')
                status = request.POST.get('status')

                post = Post.object.create(title=title, content=content, status=status, author=request.user)
                post.save()
                for f in formset:
                    try:
                        photo = Images(post=post, pic=f.cleaned_data['pic'])
                        photo.save()

                    except Exception as e:
                        break
                return HttpResponseRedirect(reverse('blog-home'))

        else:
            form = CreatePost()
            formset = ImageFormset(queryset=Images.objects.none())

            context = {
                'form': form,
                'iform': formset,
            }
            return render(request, 'mysite/post_form.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'date_posted', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
