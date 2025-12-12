from django.contrib import admin
from .models import Partnership, Customership, Product, RequestForm, ProjectReference, News, Article

@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'partner_image')

@admin.register(Customership)
class CustomershipAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_description', 'product_image')

@admin.register(RequestForm)
class RequestFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_address', 'contact_number', 'company_name', 'country', 'product_name', 'request_time')

@admin.register(ProjectReference)
class ProjectReferenceAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'location', 'contractor', 'date_time', 'layout_type', 'is_favorite', 'position')
    list_filter = ('layout_type', 'is_favorite', 'contractor')
    search_fields = ('project_name', 'location', 'contractor')
    ordering = ['position']
    fieldsets = (
        ('Project Information', {
            'fields': ('project_name', 'location', 'site_area', 'date_time', 'contractor')
        }),
        ('Display Settings', {
            'fields': ('layout_type', 'is_favorite', 'position')
        }),
        ('Images', {
            'fields': ('project_image',),
            'description': 'Add image URLs as a JSON array. Example: ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]'
        }),
    )

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('news_title', 'content')
    ordering = ['-created_at']
    fieldsets = (
        ('News Information', {
            'fields': ('news_title', 'content')
        }),
        ('Metadata', {
            'fields': ('keyword',),
            'description': 'Add keywords as a JSON array. Example: ["technology", "innovation"]'
        }),
        ('Images', {
            'fields': ('news_image',),
            'description': 'Add image URLs as a JSON array. Example: ["http://example.com/image.jpg"]'
        }),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('article_title', 'content_html')
    ordering = ['-created_at']
    fieldsets = (
        ('Article Information', {
            'fields': ('article_title', 'category', 'content_html')
        }),
        ('Content (Legacy Slate.js)', {
            'fields': ('content',),
            'classes': ('collapse',),
            'description': 'Legacy Slate.js content - usually can be left empty if using content_html'
        }),
        ('Metadata', {
            'fields': ('keyword',),
            'description': 'Add keywords as a JSON array. Example: ["research", "analysis"]'
        }),
        ('Media', {
            'fields': ('article_image', 'pdf_file'),
            'description': 'Article images (JSON array of URLs) and optional PDF attachment'
        }),
    )

