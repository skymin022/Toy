"""
URL configuration for converter project.

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
from . import views  # converter/views.py 에 main 뷰 추가

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('folder_to_txt/', include('folder_to_txt.urls')),
    path('image_to_text/', include('image_to_text.urls')),
    path('pdf_to_txt/', include('pdf_to_txt.urls')),
    path('screen_to_txt/', include('screen_to_txt.urls')),
    path('notion_converter/', include('notion_converter.urls')),

]
