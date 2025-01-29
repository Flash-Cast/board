from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board_app.models import Post, Thread
from .forms import PostForm
from .thread_form import ThreadForm
from .forms import UserRegistrationForm

# PostFormクラスをビュー関数の前に定義
class PostForm(ModelForm):
    """
    フォーム定義
    """
    class Meta:
        model = Post
        fields = ('name', 'content', 'file')

@login_required  # ログインしていない場合、ログインページにリダイレクト
def create_post(request):
    post = Post()

    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'board_app/post_form.html', {'form': form})

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 現在のユーザーを設定
            post.save()
            messages.success(request, '投稿が作成されました！')
            return redirect('board_app:thread_list')  # 適切なリダイレクト先に修正

        else:
            print(form.errors)
            return render(request, 'board_app/post_form.html', {'form': form})

def read_post(request):
    posts = Post.objects.all().order_by('id')
    return render(request, 'board_app/post_list.html', {'posts': posts})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'board_app/post_form.html', {'form': form, 'post_id': post_id})

    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

        return redirect('board_app:thread_detail', thread_id=post.thread.id)  # 編集後にスレッド詳細ページにリダイレクト

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread_id = post.thread.id
    post.delete()
    return redirect('board_app:thread_detail', thread_id=thread_id)  # 削除後にスレッド詳細ページにリダイレクト

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'board_app/thread_list.html', {'threads': threads})

@login_required  # 投稿はログインユーザーのみ可能
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user  # 現在のユーザーを設定
            post.save()
            return redirect('board_app:thread_detail', thread_id=thread.id)
    else:
        form = PostForm()

    return render(request, 'board_app/thread_detail.html', {
        'thread': thread,
        'posts': posts,
        'form': form,
    })

@login_required  # ログインしていない場合、ログインページにリダイレクト
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board_app:thread_list')  # スレッド一覧ページにリダイレクト
    else:
        form = ThreadForm()
    return render(request, 'board_app/thread_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '新しいユーザーが作成されました！')
            return redirect('login')  # 登録後にログインページにリダイレクト
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})