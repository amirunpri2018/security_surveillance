"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings  # This import is for specifying the media url
from django.conf.urls.static import static   # This import is for static url
from security_serveillance import views as view

from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

admin.site.site_header = 'LMTech Insight'
admin.site.index_title = 'LMTech Insight'
admin.site.site_title = 'LMTech Insight'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lmtech/$', view.page_load, name='page_load'),
    url(r'^predict/$', view.PredictImageObject.as_view()),
    url(r'^info/$', view.info_page, name='info_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
