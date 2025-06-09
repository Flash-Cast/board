from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board_app.models import Post, Thread, Report, Notice, Category, UserNoticeStatus ,Todo
from .forms import PostForm
from .forms import ThreadForm
from .forms import UserRegistrationForm
from .forms import TodoForm 
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReportForm
from .forms import ProfileEditForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

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
    category_id = request.GET.get('category')
    selected_category = None
    notices = Notice.objects.all().order_by('-created_at')[:5]  # 最新5件のお知らせを取得
    if category_id:
        threads = Thread.objects.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        threads = Thread.objects.all()
    categories = Category.objects.all()
    return render(request, 'board_app/thread_list.html', {'threads': threads, 'notices': notices, 'categories': categories,'selected_category': selected_category})

@login_required  # 投稿はログインユーザーのみ可能
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    notices = Notice.objects.all().order_by('-created_at')[:5] 
    posts = thread.posts.all()
    for post in posts:
        post.is_admin = post.author.is_superuser or post.author.groups.filter(name="管理者").exists()

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
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
        'notices': notices
    })

@login_required  # ログインしていない場合、ログインページにリダイレクト
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
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
            user = form.save()
            login(request, user)  # 新規登録後に自動ログイン
            messages.success(request, '新しいユーザーが作成されました！')
            return redirect('board_app:thread_list')  # スレッド一覧ページにリダイレクト
        else:
            messages.error(request, '入力内容に誤りがあります。')

    else:
        form = UserRegistrationForm()

    return render(request, 'board_app/register.html', {'form': form})


def about(request):
    return render(request, 'board_app/about.html')

def terms_of_service(request):
    return render(request, 'board_app/terms_of_service.html')

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
            return redirect('board_app:profile')  # 編集後にプロフィールページにリダイレクト
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

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 投稿者のみ削除可能
    if request.user == post.author:
        post.delete()
        messages.success(request, "投稿を削除しました。")
    else:
        messages.error(request, "この投稿を削除する権限がありません。")

    return redirect('board_app:thread_list')  # 削除後のリダイレクト先を設定


@login_required
@require_POST
def mark_as_read(request, notice_id):
    """お知らせを既読としてマークするAPIビュー"""
    try:
        # ログイン中のユーザーと、URLから受け取ったnotice_idを使って、
        # 既読状態(UserNoticeStatus)を更新または新規作成します。
        # レコードがあれば更新、なければ作成してくれる便利なメソッドです。
        UserNoticeStatus.objects.update_or_create(
            user=request.user,
            notice_id=notice_id,
            defaults={'is_read': True} # 既読(True)に設定
        )

        # 処理が成功したことをJavaScriptに伝える
        return JsonResponse({'success': True})

    except Exception as e:
        # 何かエラーが起きた場合
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@login_required
def home(request):
    """ホーム画面"""
    # --- POSTリクエスト（フォームが送信された時）の処理 ---
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save() # データをデータベースに保存
            return redirect('board_app:home') # ホーム画面にリダイレクト
    # --- GETリクエスト（ページが普通に表示された時）の処理 ---
    else:
        form = TodoForm() # 空のフォームを準備

    # --- 表示データの取得（ここは変更なし） ---
    latest_notices = Notice.objects.order_by('-created_at')[:5]
    today = timezone.localdate()
    three_days_ago = today - timedelta(days=3)
    three_days_later = today + timedelta(days=3)
    todo_list = Todo.objects.filter(due_date__gt=three_days_ago)
    
    # ↓ここから絞り込みのロジック↓
    # まずは期限切れでないTodoをすべて取得する準備
    base_query = Todo.objects.filter(due_date__gt=three_days_ago)

    # URLから'grade'の値を取得する (例: '1', '2'など)
    selected_grade = request.GET.get('grade') 

    if selected_grade:
        # もし'grade'の値があれば、それでさらにデータを絞り込む
        todo_list = base_query.filter(grade=selected_grade)
    else:
        # 'grade'の値がなければ（「全学年」クリック時など）、すべてのデータを表示
        todo_list = base_query
    # ↑ここまでが絞り込みのロジック↑

    for todo in todo_list:
        todo.is_overdue = todo.due_date < today
        todo.is_warning = today <= todo.due_date <= three_days_later

    context = {
        'latest_notices': latest_notices,
        'todo_list': todo_list,
        'form': form,
        'selected_grade': selected_grade, # contextにフォームを追加
    }
    return render(request, 'board_app/home.html', context)