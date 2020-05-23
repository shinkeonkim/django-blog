from django.contrib import admin
from django.urls import path, include
import BlogApp.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',BlogApp.views.post_list),
    path('blog/', include('BlogApp.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)