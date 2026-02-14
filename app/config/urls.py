"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import error_views

handler400 = "config.error_views.bad_request"
handler403 = "config.error_views.permission_denied"
handler404 = "config.error_views.page_not_found"
handler500 = "config.error_views.server_error"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('knowledgeapp.urls')),
    path('', include('accounts.urls')),
    #Djangoが元々持っているauthという認証機能を追加
    #これがあるとhtmlでaccounts:login,accounts:logoutと指定しなくて済む
    path('', include('django.contrib.auth.urls')),
    path("errors/<int:code>/", error_views.preview_error, name="error_preview"),
    path("errors/405/", error_views.method_not_allowed, name="error_405"),
    path("errors/429/", error_views.too_many_requests, name="error_429"),
    path("errors/502/", error_views.bad_gateway, name="error_502"),
    path("errors/503/", error_views.service_unavailable, name="error_503"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
