from django.db import models

class Partnership(models.Model):
    partner_name = models.CharField(max_length=255, null=True, blank=True)
    partner_image = models.JSONField(default=list)
    def __str__(self):
        return self.partner_name

class Customership(models.Model):
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_image = models.JSONField(default=list)

class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False, blank=False)
    product_image = models.JSONField(default=list)
    product_description = models.CharField(max_length=525, null=False, blank=False)
    success = models.JSONField(default=list)
    benefit = models.JSONField(default=list)
    performance = models.JSONField(default=list)
    def __str__(self):
        return self.product_name

class RequestForm(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    email_address = models.CharField(max_length=255, null=False, blank=False)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    request_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
         return f"Request from {self.full_name} for {self.product.product_name if self.product else 'No product'}"
    
class ProjectReference(models.Model):
    project_name = models.CharField(max_length=255, null=False, blank=False)
    project_image = models.JSONField(default=list)
    location = models.CharField(max_length=255, null=False, blank=False)
    site_area = models.CharField(max_length=255, null=False, blank=False)
    date_time = models.CharField(max_length=255, null=False, blank=False)
    contractor = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.project_name

class News(models.Model):
    news_title = models.CharField(max_length=255, null=False, blank=False)
    news_image = models.JSONField(default=list)
    keyword = models.JSONField(null=True, blank=True, default=list)
    content = models.TextField(null=False, blank=False)
    def __str__(self):
        return self.news_title
