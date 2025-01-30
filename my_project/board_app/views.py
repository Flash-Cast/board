from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board_app.models import Post, Thread, Report
from .forms import PostForm
from .thread_form import ThreadForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReportForm
from .forms import ProfileEditForm
from django.contrib.auth.decorators import user_passes_test

# PostFormクラスをビュー関数の前に定義
class PostForm(ModelForm):
    """
    フォーム定義
    """
    class Meta:
        model = Post
        fields = ('name', 'content', 'file')



@login_required
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'board_app/thread_list.html', {'threads': threads})

@login_required  # 投稿はログインユーザーのみ可能
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()
    for post in posts:
        post.is_admin = post.author.is_superuser or post.author.groups.filter(name="管理者").exists()
        
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

def about(request):
    return render(request, 'board_app/about.html')

@staff_member_required  # 管理者だけが実行可能
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # アカウント停止
    user.save()
    return redirect('admin:index')  # Django管理画面にリダイレクト

@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.thread:
        messages.error(request, '関連するスレッドが見つかりません。')
        return redirect('board_app:thread_list')  # スレッド一覧にリダイレクト

    thread = post.thread  # threadがNoneでないことを保証
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_post = post
            report.reported_by = request.user
            report.save()
            return redirect('board_app:thread_list')
    else:
        form = ReportForm()
    return render(request, 'board_app/report_post.html', {'form': form,'post':post})

@login_required
def profile_edit(request):
    # 現在のユーザーを取得
    user = request.user

    if request.method == 'POST':
        # フォームに POST データを渡して、ユーザーが送信した情報を処理
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # ユーザー情報を保存
            messages.success(request, 'プロフィールが更新されました。')
            return redirect('profile')  # 編集後にプロフィールページにリダイレクト
    else:
        # ユーザーの現在の情報でフォームを表示
        form = ProfileEditForm(instance=user)

    return render(request, 'board_app/profile_edit.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'board_app/profile.html', {'user': request.user})

def admin_required(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name="管理者").exists())

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'board_app/admin_dashboard.html')