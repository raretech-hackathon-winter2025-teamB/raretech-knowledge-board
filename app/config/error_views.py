from django.http import HttpResponse
from django.shortcuts import render


ERROR_META = {
    400: ("400 Bad Request", "リクエストの形式が正しくありません。入力内容を確認してください。", False),
    403: ("403 Forbidden", "このページへのアクセス権限がありません。", False),
    404: ("404 Not Found", "ページが見つかりません。URLを確認してください。", False),
    405: ("405 Method Not Allowed", "この操作は許可されていません。送信方法を確認してください。", False),
    429: ("429 Too Many Requests", "アクセスが集中しています。時間をおいて再試行してください。", True),
    500: ("500 Internal Server Error", "サーバで問題が発生しました。時間をおいて再試行してください。", True),
    502: ("502 Bad Gateway", "上流サービスへの接続に失敗しました。しばらくしてから再試行してください。", True),
    503: ("503 Service Unavailable", "現在メンテナンス中です。しばらくしてから再試行してください。", True),
}


def _context(request, code):
    title, message, show_retry = ERROR_META[code]
    return {
        "status_code": code,
        "status_title": title,
        "status_message": message,
        "show_retry": show_retry,
        "request_path": request.path,
    }


def _render_error(request, code):
    context = _context(request, code)
    if request.headers.get("HX-Request") == "true":
        response = render(request, "errors/partials/error_panel.html", context=context, status=code)
        response["HX-Reselect"] = "#error-panel"
        response["HX-Retarget"] = "main"
        response["HX-Reswap"] = "innerHTML"
        response["Cache-Control"] = "no-store"
        return response

    response = render(request, f"errors/{code}.html", context=context, status=code)
    response["Cache-Control"] = "no-store"
    return response


def bad_request(request, exception):
    return _render_error(request, 400)


def permission_denied(request, exception):
    return _render_error(request, 403)


def page_not_found(request, exception):
    return _render_error(request, 404)


def server_error(request):
    return _render_error(request, 500)


def method_not_allowed(request):
    return _render_error(request, 405)


def too_many_requests(request):
    return _render_error(request, 429)


def bad_gateway(request):
    return _render_error(request, 502)


def service_unavailable(request):
    return _render_error(request, 503)


def preview_error(request, code):
    if code not in ERROR_META:
        return HttpResponse("Unknown status code", status=400)
    return _render_error(request, code)
