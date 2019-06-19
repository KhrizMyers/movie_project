from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.api.viewsets import TodoViewSet

router = DefaultRouter()
router.register('', TodoViewSet, base_name='todos')
urlpatterns = [
    # URLs Por mapeo
    path('movies/', TodoViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-detail-actions'),
    path('movies/<int:pk>', TodoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
                                                 'patch': 'partial_update'}), name='movie-detail-actions1'),
    # URLs por Router
    path('router/', include(router.urls))
]
