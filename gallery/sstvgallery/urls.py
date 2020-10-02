from django.urls import include, path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)


urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<int:image_id>/', views.detail, name='detail'),
    path('<int:image_id>/comment', views.comment, name='comment'),
    path('<int:image_id>/vote', views.vote, name='vote'),
    path('<int:image_id>/results', views.results, name='results'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('about/', views.about, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
