from .models import Notice, UserNoticeStatus # UserNoticeStatus をインポート

def common_notices(request):
    # お知らせのリストを取得
    notices = Notice.objects.order_by('-created_at')[:5]

    # ユーザーがログインしている場合のみ、既読情報を付与する
    if request.user.is_authenticated:
        # ログインユーザーが既読にしたお知らせのIDリストを先に取得しておく
        read_notice_ids = UserNoticeStatus.objects.filter(
            user=request.user, 
            is_read=True
        ).values_list('notice_id', flat=True)

        # 取得した各お知らせ(notice)をループで処理
        for notice in notices:
            # お知らせのIDが、既読IDリストにあれば is_read を True にする
            notice.is_read = notice.id in read_notice_ids
    else:
        # ログインしていないユーザーには、すべて未読として見せる
        for notice in notices:
            notice.is_read = False

    return {'notices': notices}