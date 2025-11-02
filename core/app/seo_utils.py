from django.contrib.contenttypes.models import ContentType
from .models import SEO, DefaultSeoSettings
from django.utils.html import strip_tags
import json

class SEOHelper:
    """Helper class for SEO operations"""
    
    @staticmethod
    def get_page_seo_data(obj=None, page_type='default', request=None, **kwargs):
        """
        Get comprehensive SEO data for a page
        
        Args:
            obj: Model instance with SEO relationship (e.g., BlogPost, Service)
            page_type: Type of page ('home', 'blog', 'services', etc.)
            request: Django request object for building absolute URLs
            **kwargs: Override values
        
        Returns:
            dict: SEO data including page_seo, default_seo, and schema
        """
        default_seo = DefaultSeoSettings.objects.filter(is_active=True).first()
        
        # Get SEO data from object if it has SEO relationship
        if obj and hasattr(obj, 'seo') and obj.seo:
            page_seo = obj.seo
        elif obj:
            # Fallback: create mock SEO object from model's get_seo_* methods
            page_seo = type('SEO', (), {
                'meta_title': getattr(obj, 'get_seo_title', lambda: str(obj))(),
                'meta_description': getattr(obj, 'get_seo_description', lambda: '')(),
                'meta_keywords': kwargs.get('meta_keywords', ''),
                'get_og_title': lambda: getattr(obj, 'get_seo_title', lambda: str(obj))(),
                'get_og_description': lambda: getattr(obj, 'get_seo_description', lambda: '')(),
                'get_twitter_title': lambda: getattr(obj, 'get_seo_title', lambda: str(obj))(),
                'get_twitter_description': lambda: getattr(obj, 'get_seo_description', lambda: '')(),
                'og_image': getattr(obj, 'cover_image', None) or getattr(obj, 'feature_image', None) or getattr(obj, 'image', None),
                'get_twitter_image': lambda: None,
                'robots': 'index, follow',
                'canonical_url': kwargs.get('canonical_url', ''),
                'schema_type': kwargs.get('schema_type', ''),
                'focus_keyword': kwargs.get('focus_keyword', ''),
            })()
        else:
            # Use page-type defaults
            page_seo = SEOHelper._get_page_defaults(page_type, default_seo, **kwargs)
        
        # Generate schema markup
        schema_markup = SEOHelper.generate_schema_markup(obj, page_seo, default_seo, request)
        
        return {
            'page_seo': page_seo,
            'default_seo': default_seo,
            'schema_markup': schema_markup,
        }
    
    @staticmethod
    def _get_page_defaults(page_type, default_seo, **kwargs):
        """Get default SEO data for different page types"""
        site_name = default_seo.site_name if default_seo else 'Blue Diamond Service Center'
        
        defaults = {
            'home': {
                'meta_title': f"{site_name} - Professional Appliance Repair Services Nepal",
                'meta_description': "Expert appliance repair services in Nepal. AC, refrigerator, washing machine, geyser repair with certified technicians and genuine parts.",
                'meta_keywords': "appliance repair Nepal, AC repair Kathmandu, refrigerator repair, washing machine service, geyser installation",
            },
            'services': {
                'meta_title': f"Our Services - {site_name}",
                'meta_description': "Professional appliance repair and maintenance services. Expert technicians, genuine parts, and reliable service across Nepal.",
                'meta_keywords': "appliance services, repair services Nepal, maintenance services",
            },
            'blog': {
                'meta_title': f"Blog - {site_name}",
                'meta_description': "Latest tips, guides, and news about appliance repair and maintenance from our expert technicians.",
                'meta_keywords': "appliance tips, repair guides, maintenance blog",
            },
            'training': {
                'meta_title': f"Training Courses - {site_name}",
                'meta_description': "Professional appliance repair training courses. Learn from certified technicians and start your career in appliance repair.",
                'meta_keywords': "appliance repair training, technical courses Nepal, CTVT courses",
            },
            'about': {
                'meta_title': f"About Us - {site_name}",
                'meta_description': "Learn about our professional appliance repair services, experienced team, and commitment to quality service in Nepal.",
                'meta_keywords': "about us, appliance repair company, professional technicians Nepal",
            },
            'contact': {
                'meta_title': f"Contact Us - {site_name}",
                'meta_description': "Get in touch with our appliance repair experts. Call us for quick service or visit our service center in Nepal.",
                'meta_keywords': "contact, appliance repair service, phone number, address Nepal",
            },
        }
        
        page_defaults = defaults.get(page_type, defaults['home'])
        page_defaults.update(kwargs)
        
        # Create mock SEO object
        return type('SEO', (), {
            'meta_title': page_defaults['meta_title'],
            'meta_description': page_defaults['meta_description'],
            'meta_keywords': page_defaults['meta_keywords'],
            'get_og_title': lambda: page_defaults['meta_title'],
            'get_og_description': lambda: page_defaults['meta_description'],
            'get_twitter_title': lambda: page_defaults['meta_title'],
            'get_twitter_description': lambda: page_defaults['meta_description'],
            'og_image': default_seo.default_og_image if default_seo else None,
            'get_twitter_image': lambda: default_seo.default_og_image if default_seo else None,
            'robots': 'index, follow',
            'canonical_url': '',
            'schema_type': page_defaults.get('schema_type', 'WebPage'),
            'focus_keyword': page_defaults.get('focus_keyword', ''),
        })()
    
    @staticmethod
    def generate_schema_markup(obj, page_seo, default_seo, request=None):
        """Generate Schema.org JSON-LD markup"""
        schema_type = getattr(page_seo, 'schema_type', None)
        if not schema_type:
            return ""
        
        base_url = request.build_absolute_uri('/') if request else 'https://bluediamondservicecenter.com/'
        
        schema = {
            "@context": "https://schema.org",
            "@type": schema_type,
        }
        
        # Add common fields
        if hasattr(page_seo, 'meta_title'):
            schema["name"] = page_seo.meta_title
        if hasattr(page_seo, 'meta_description'):
            schema["description"] = page_seo.meta_description
        
        # Type-specific fields
        if schema_type in ['Article', 'BlogPosting']:
            if obj:
                schema["headline"] = getattr(obj, 'title', '')
                schema["datePublished"] = getattr(obj, 'published_at', getattr(obj, 'created_at', '')).isoformat() if hasattr(obj, 'published_at') or hasattr(obj, 'created_at') else ''
                schema["dateModified"] = getattr(obj, 'updated_at', '').isoformat() if hasattr(obj, 'updated_at') else ''
                if hasattr(obj, 'cover_image') and obj.cover_image:
                    schema["image"] = base_url + obj.cover_image.url if obj.cover_image else ''
        
        elif schema_type == 'Service':
            if obj:
                schema["serviceType"] = getattr(obj, 'name', '')
                schema["provider"] = {
                    "@type": "LocalBusiness",
                    "name": default_seo.site_name if default_seo else "Blue Diamond Service Center"
                }
        
        elif schema_type == 'Course':
            if obj:
                schema["name"] = getattr(obj, 'title', '')
                schema["description"] = getattr(obj, 'short_description', '')
                if hasattr(obj, 'duration') and obj.duration:
                    schema["timeRequired"] = obj.duration
        
        return json.dumps(schema, indent=2) if schema.get('@type') else ""


def generate_breadcrumb_schema(breadcrumbs, request=None):
    """
    Generate JSON-LD breadcrumb schema
    
    Args:
        breadcrumbs: List of tuples [(name, url), ...]
        request: Django request object for building absolute URLs
    
    Returns:
        str: JSON-LD breadcrumb schema
    """
    if not breadcrumbs:
        return ""
    
    base_url = request.build_absolute_uri('/') if request else 'https://bluediamondservicecenter.com/'
    
    items = []
    for i, (name, url) in enumerate(breadcrumbs, 1):
        # Make URL absolute if it's relative
        if url and not url.startswith('http'):
            url = base_url.rstrip('/') + url
        
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    return json.dumps(schema, indent=2)


def clean_text_for_seo(text, max_length=160):
    """
    Clean and truncate text for SEO purposes
    
    Args:
        text: Text to clean
        max_length: Maximum length
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Strip HTML tags
    clean_text = strip_tags(text)
    
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    
    # Truncate if needed
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return clean_text