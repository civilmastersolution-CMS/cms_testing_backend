from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartnershipViewSet, CustomershipViewSet, ProductViewSet, RequestFormViewSet, ProjectReferenceViewSet, NewsViewSet

router = DefaultRouter()
router.register(r'partnerships', PartnershipViewSet)
router.register(r'customerships', CustomershipViewSet)
router.register(r'products', ProductViewSet)
router.register(r'requestforms', RequestFormViewSet)
router.register(r'projectreferences', ProjectReferenceViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]