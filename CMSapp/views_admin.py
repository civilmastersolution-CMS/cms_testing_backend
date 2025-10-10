from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Partnership, Customership, Product, RequestForm, ProjectReference, News
from .serializers import PartnershipSerializer, CustomershipSerializer, ProductSerializer, RequestFormSerializer, ProjectReferenceSerializer, NewsSerializer

class AdminPartnershipViewSet(viewsets.ModelViewSet):
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer
    permission_classes = [IsAdminUser]

class AdminCustomershipViewSet(viewsets.ModelViewSet):
    queryset = Customership.objects.all()
    serializer_class = CustomershipSerializer
    permission_classes = [IsAdminUser]

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminRequestFormViewSet(viewsets.ModelViewSet):
    queryset = RequestForm.objects.all()
    serializer_class = RequestFormSerializer
    permission_classes = [IsAdminUser]

class AdminProjectReferenceViewSet(viewsets.ModelViewSet):
    queryset = ProjectReference.objects.all()
    serializer_class = ProjectReferenceSerializer
    permission_classes = [IsAdminUser]

class AdminNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]