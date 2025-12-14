from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Partnership,Product, RequestForm, ProjectReference, News, Article
from rest_framework import status
from .serializers import PartnershipSerializer, ProductSerializer, RequestFormSerializer, ProjectReferenceSerializer, NewsSerializer, ArticleSerializer
import os
import logging
import re
import logging
import base64

class AdminPartnershipViewSet(viewsets.ModelViewSet):
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer
    permission_classes = [IsAdminUser]

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('position')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminRequestFormViewSet(viewsets.ModelViewSet):
    queryset = RequestForm.objects.all()
    serializer_class = RequestFormSerializer
    permission_classes = [IsAdminUser]
 
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update the status of a request form."""
        request_form = self.get_object()
        status = request.data.get('status')
        if status not in ['pending', 'complete']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        request_form.status = status
        request_form.save()
        
        serializer = self.get_serializer(request_form)
        return Response(serializer.data)

class AdminProjectReferenceViewSet(viewsets.ModelViewSet):
    queryset = ProjectReference.objects.all().order_by('position')
    serializer_class = ProjectReferenceSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle favorite status for a project reference with max limitof 4."""
        project = self.get_object()
        if project.is_favorite: # If currently favorite, remove from favorites
            project.is_favorite = False
            project.save()
            return Response({
                'message': 'Removed from favorites',
                'is_favorite': False,
                'favorites_count': ProjectReference.objects.filter(is_favorite=True).count()
            })
        else: # Check if we already have 4 favorites
            current_favorite_count = ProjectReference.objects.filter(is_favorite=True).count()
            if current_favorite_count >= 4:
                return Response({
                    'error': 'Maximum of 4 favorite projects allowed.',
                    'favorite_count': current_favorite_count
                }, status=status.HTTP_400_BAD_REQUEST)
            # Add to favorite
            project.is_favorite = True
            project.save()
            return Response({
                'message': 'Added to favorites',
                'is_favorite': True,
                'favorite_count': ProjectReference.objects.filter(is_favorite=True).count()
            })
        
        @action(detail=False, methods=['get'])
        def favorites(self, request):
            """Get all favorite project references"""
            favorites = ProjectReference.objects.filter(is_favorite=True)
            serializer = self.get_serializer(favorites, many=True)
            return Response(serializer.data)

class AdminNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        """Handle news creation - serializer handles all parsing"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"News serializer validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Handle news update - serializer handles all parsing"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)


class AdminArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """Handle article creation with PDF file upload and images"""
        data = request.data.copy()
        
        # Handle PDF file if provided
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            data['pdf_file'] = pdf_file
        
        # Handle article images if provided
        images = request.FILES.getlist('article_image')
        if images:
            # Process images and convert to base64 for storage
            image_data_list = []
            for image in images:
                import base64
                image_content = image.read()
                encoded_image = base64.b64encode(image_content).decode('utf-8')
                data_url = f"data:{image.content_type};base64,{encoded_image}"
                image_data_list.append(data_url)
            data['article_image'] = image_data_list
        
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Handle article update with PDF file upload and images"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        
        # Handle PDF file if provided
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            data['pdf_file'] = pdf_file
        
        # Handle article images if provided  
        images = request.FILES.getlist('article_image')
        if images:
            # Process images and convert to base64 for storage
            image_data_list = []
            for image in images:
                import base64
                image_content = image.read()
                encoded_image = base64.b64encode(image_content).decode('utf-8')
                data_url = f"data:{image.content_type};base64,{encoded_image}"
                image_data_list.append(data_url)
            data['article_image'] = image_data_list
        
        serializer = self.get_serializer(instance, data=data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def upload_article(self, request):
        """Upload HTML file and images, process them, and create an article."""
        try:
            # Get form data
            html_file = request.FILES.get('html_file')
            images = request.FILES.getlist('images')
            pdf_file = request.FILES.get('pdf_file')  # Add PDF file support
            article_title = request.data.get('article_title')
            keyword = request.data.get('keyword')
            category = request.data.get('category')

            logging.info(f"Received article upload: title={article_title}, html={bool(html_file)}, images={len(images)}, pdf={bool(pdf_file)}")

            if not article_title:
                return Response({'error': 'Article title is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize content variables
            html_content = ""
            if html_file:
                # Read HTML content
                html_content = html_file.read().decode('utf-8')
                print(f"HTML content length: {len(html_content)}")
            
            # Process images and update HTML
            image_data_list = []
            if images:
                # Create a mapping of original filenames to data URLs for HTML replacement
                image_map = {}
                
                for image in images:
                    # Read image content and encode as base64
                    image_content = image.read()
                    encoded_image = base64.b64encode(image_content).decode('utf-8')
                    
                    # Create data URL
                    content_type = image.content_type or 'image/jpeg'
                    data_url = f"data:{content_type};base64,{encoded_image}"
                    
                    # Store image data in database format
                    image_data = {
                        'name': image.name,
                        'data': encoded_image,
                        'content_type': content_type,
                        'data_url': data_url
                    }
                    image_data_list.append(image_data)
                    
                    # Store mapping for HTML replacement
                    # Try multiple variations of the original filename
                    original_name = image.name
                    variations = [
                        original_name,  # original
                        original_name.lower(),  # lowercase
                        os.path.splitext(original_name)[0],  # without extension
                        os.path.splitext(original_name)[0].lower(),  # lowercase without extension
                        # Try different extensions
                        os.path.splitext(original_name)[0] + '.png',
                        os.path.splitext(original_name)[0] + '.jpg',
                        os.path.splitext(original_name)[0] + '.jpeg',
                        os.path.splitext(original_name)[0] + '.gif',
                    ]
                    
                    for variation in variations:
                        image_map[variation] = data_url

                # Replace image src attributes in HTML
                def replace_image_src(match):
                    src = match.group(1)  # This is now the src value without quotes
                    
                    # Skip if already a data URL (base64) or external URL
                    if src.startswith('data:') or src.startswith('http://') or src.startswith('https://'):
                        return match.group(0)
                    
                    # Try different ways to match the filename
                    possible_names = [
                        src,  # full path
                        os.path.basename(src),  # just filename
                        os.path.basename(src).lower(),  # lowercase filename
                        os.path.splitext(os.path.basename(src))[0],  # without extension
                        os.path.splitext(os.path.basename(src))[0].lower(),  # lowercase without extension
                        # Try variations with different extensions
                        os.path.splitext(os.path.basename(src))[0] + '.png',
                        os.path.splitext(os.path.basename(src))[0] + '.jpg',
                        os.path.splitext(os.path.basename(src))[0] + '.jpeg',
                        os.path.splitext(os.path.basename(src))[0] + '.gif',
                    ]
                    
                    for name in possible_names:
                        if name in image_map:
                            # Replace the src value in the match
                            return match.group(0).replace(src, image_map[name])
                    
                    return match.group(0)  # No replacement found
                
                # Replace all img src attributes if HTML content exists
                if html_content:
                    img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'
                    html_content = re.sub(img_pattern, replace_image_src, html_content, flags=re.IGNORECASE)
            
            # Create the article
            article = Article.objects.create(
                article_title=article_title,
                keyword=keyword.split(',') if keyword else [],
                category=category,
                content=[],  # Required field, empty for HTML articles
                content_html=html_content,  # Store HTML content
                article_image=image_data_list  # Store list of image data dicts
            )
            
            # Handle PDF file upload separately
            if pdf_file:
                try:
                    article.pdf_file = pdf_file
                    article.save()
                    logging.info(f"PDF file saved: {article.pdf_file.name}")
                except Exception as pdf_error:
                    logging.error(f"Error saving PDF file: {pdf_error}")
                    # Continue even if PDF fails

            # Get serializer with request context for proper URL generation
            serializer = self.get_serializer(article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logging.error(f"Error creating article: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
