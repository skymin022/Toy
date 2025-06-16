from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kr/', include('stock_kr.urls')),
    path('global/', include('stock_global.urls')),
    path('dashboard/', include('dashboard.urls')),
]