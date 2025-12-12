from django.core.management.base import BaseCommand
from CMSapp.models import ProjectReference, News, Article
import json

class Command(BaseCommand):
    help = 'Import data from JSON files'

    def add_arguments(self, parser):
        parser.add_argument('--type', type=str, help='Type of data to import: projects, news, or articles')
        parser.add_argument('--file', type=str, help='Path to JSON file containing data')

    def handle(self, *args, **options):
        if not options['type'] or not options['file']:
            self.stdout.write(self.style.ERROR('Please provide both --type and --file arguments'))
            return

        try:
            with open(options['file'], 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {options["file"]}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON in file: {options["file"]}'))
            return

        if options['type'] == 'projects':
            self.import_projects(data)
        elif options['type'] == 'news':
            self.import_news(data)
        elif options['type'] == 'articles':
            self.import_articles(data)
        else:
            self.stdout.write(self.style.ERROR('Type must be: projects, news, or articles'))

    def import_projects(self, data):
        """
        Expected format:
        [
            {
                "project_name": "Project Name",
                "location": "Location",
                "site_area": "1000 sq m",
                "date_time": "2024-01-01",
                "contractor": "Contractor Name",
                "layout_type": 1,
                "is_favorite": false,
                "position": 1,
                "project_image": ["image_url1", "image_url2"]
            }
        ]
        """
        created_count = 0
        for item in data:
            project, created = ProjectReference.objects.get_or_create(
                project_name=item.get('project_name', ''),
                defaults={
                    'location': item.get('location', ''),
                    'site_area': item.get('site_area', ''),
                    'date_time': item.get('date_time', ''),
                    'contractor': item.get('contractor', ''),
                    'layout_type': item.get('layout_type', 1),
                    'is_favorite': item.get('is_favorite', False),
                    'position': item.get('position', 1),
                    'project_image': item.get('project_image', []),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created project: {project.project_name}')
            else:
                self.stdout.write(f'Project already exists: {project.project_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Imported {created_count} new projects'))

    def import_news(self, data):
        """
        Expected format:
        [
            {
                "news_title": "News Title",
                "content": "News content here",
                "keyword": ["keyword1", "keyword2"],
                "news_image": ["image_url"]
            }
        ]
        """
        created_count = 0
        for item in data:
            news, created = News.objects.get_or_create(
                news_title=item.get('news_title', ''),
                defaults={
                    'content': item.get('content', ''),
                    'keyword': item.get('keyword', []),
                    'news_image': item.get('news_image', []),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created news: {news.news_title}')
            else:
                self.stdout.write(f'News already exists: {news.news_title}')
        
        self.stdout.write(self.style.SUCCESS(f'Imported {created_count} new news items'))

    def import_articles(self, data):
        """
        Expected format:
        [
            {
                "article_title": "Article Title",
                "category": "Category",
                "content_html": "<p>Article content in HTML</p>",
                "keyword": ["keyword1", "keyword2"],
                "article_image": ["image_url"]
            }
        ]
        """
        created_count = 0
        for item in data:
            article, created = Article.objects.get_or_create(
                article_title=item.get('article_title', ''),
                defaults={
                    'category': item.get('category', ''),
                    'content_html': item.get('content_html', ''),
                    'keyword': item.get('keyword', []),
                    'article_image': item.get('article_image', []),
                    'content': item.get('content', []),  # Legacy field
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created article: {article.article_title}')
            else:
                self.stdout.write(f'Article already exists: {article.article_title}')
        
        self.stdout.write(self.style.SUCCESS(f'Imported {created_count} new articles'))