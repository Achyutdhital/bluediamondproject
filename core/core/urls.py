"""
URL configuration for core project.

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import Http404
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('app.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Custom error handlers
handler404 = 'app.views.custom_404_view'

# Custom media serving for cPanel
def serve_media(request, path):
    media_root = settings.MEDIA_ROOT
    if os.path.exists(os.path.join(media_root, path)):
        return serve(request, path, document_root=media_root)
    raise Http404("Media file not found")

# Add media URL pattern
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_media),
]

# Fallback static serving
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
