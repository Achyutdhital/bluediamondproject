from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Services, BlogPost, TrainingCourse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'services', 'gallery', 'training_courses', 'blog_list', 'contact', 'enquiry']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == 'home':
            return 1.0
        elif item in ['services', 'about', 'contact']:
            return 0.9
        return 0.8

class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Services.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/services/{obj.slug}/'

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/blog/{obj.slug}/'

class TrainingCourseSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return TrainingCourse.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/training/{obj.slug}/'