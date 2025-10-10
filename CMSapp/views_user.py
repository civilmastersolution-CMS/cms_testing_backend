from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Partnership, Customership, Product, RequestForm, ProjectReference, News
from .serializers import PartnershipSerializer, CustomershipSerializer, ProductSerializer, RequestFormSerializer, ProjectReferenceSerializer, NewsSerializer

class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

class PartnershipViewSet(ReadOnlyViewSet):
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer
    
class CustomershipViewSet(ReadOnlyViewSet):
    queryset = Customership.objects.all()
    serializer_class = CustomershipSerializer

class ProductViewSet(ReadOnlyViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RequestFormViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = RequestForm.objects.all().order_by('-request_time')  
    serializer_class = RequestFormSerializer
    permission_classes = [AllowAny]

class ProjectReferenceViewSet(ReadOnlyViewSet):
    queryset = ProjectReference.objects.all()
    serializer_class = ProjectReferenceSerializer

class NewsViewSet(ReadOnlyViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer