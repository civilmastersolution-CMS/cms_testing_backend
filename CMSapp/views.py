from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Partnership, Customership, Product, RequestForm, ProjectReference, News
from .serializers import PartnershipSerializer, CustomershipSerializer, ProductSerializer, RequestFormSerializer, ProjectReferenceSerializer, NewsSerializer

class PartnershipViewSet(viewsets.ModelViewSet):
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer

class CustomershipViewSet(viewsets.ModelViewSet):
    queryset = Customership.objects.all()
    serializer_class = CustomershipSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RequestFormViewSet(viewsets.ModelViewSet):
    queryset = RequestForm.objects.all().order_by('-request_time')  
    serializer_class = RequestFormSerializer
    permission_classes = [AllowAny]

class ProjectReferenceViewSet(viewsets.ModelViewSet):
    queryset = ProjectReference.objects.all()
    serializer_class = ProjectReferenceSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer