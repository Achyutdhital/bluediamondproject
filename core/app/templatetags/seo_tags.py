from django import template
from django.utils.safestring import mark_safe
from app.models import DefaultSeoSettings
import json

register = template.Library()


@register.inclusion_tag('app/seo/meta_tags.html', takes_context=True)
def render_seo_meta_tags(context, page_seo=None, default_seo=None):
    """
    Render all SEO meta tags including Open Graph, Twitter Cards, and Schema.org
    
    Usage in template:
        {% load seo_tags %}
        {% render_seo_meta_tags page_seo=page_seo default_seo=default_seo %}
    """
    request = context.get('request')
    
    # Get default SEO settings if not provided
    if not default_seo:
        default_seo = DefaultSeoSettings.objects.filter(is_active=True).first()
    
    # Build absolute URL for canonical and og:url
    absolute_url = ''
    if request:
        absolute_url = request.build_absolute_uri()
    
    return {
        'page_seo': page_seo,
        'default_seo': default_seo,
        'absolute_url': absolute_url,
        'request': request,
    }


@register.simple_tag
def render_schema_markup(schema_markup):
    """
    Render Schema.org JSON-LD markup
    
    Usage:
        {% render_schema_markup schema_markup %}
    """
    if schema_markup:
        return mark_safe(f'<script type="application/ld+json">{schema_markup}</script>')
    return ''


@register.simple_tag
def render_breadcrumb_schema(breadcrumbs, request=None):
    """
    Generate and render breadcrumb schema
    
    Usage:
        {% render_breadcrumb_schema breadcrumbs request %}
    """
    if not breadcrumbs:
        return ''
    
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
    
    json_output = json.dumps(schema, indent=2)
    return mark_safe(f'<script type="application/ld+json">{json_output}</script>')


@register.simple_tag
def get_default_seo():
    """
    Get default SEO settings
    
    Usage:
        {% get_default_seo as default_seo %}
    """
    return DefaultSeoSettings.objects.filter(is_active=True).first()


@register.filter
def get_og_image_url(seo_obj, default_seo=None):
    """
    Get Open Graph image URL with fallback
    
    Usage:
        {{ page_seo|get_og_image_url:default_seo }}
    """
    if seo_obj and hasattr(seo_obj, 'og_image') and seo_obj.og_image:
        return seo_obj.og_image.url
    if default_seo and hasattr(default_seo, 'default_og_image') and default_seo.default_og_image:
        return default_seo.default_og_image.url
    return ''


@register.filter
def get_twitter_image_url(seo_obj, default_seo=None):
    """
    Get Twitter image URL with fallback
    
    Usage:
        {{ page_seo|get_twitter_image_url:default_seo }}
    """
    if seo_obj and hasattr(seo_obj, 'twitter_image') and seo_obj.twitter_image:
        return seo_obj.twitter_image.url
    if seo_obj and hasattr(seo_obj, 'og_image') and seo_obj.og_image:
        return seo_obj.og_image.url
    if default_seo and hasattr(default_seo, 'default_og_image') and default_seo.default_og_image:
        return default_seo.default_og_image.url
    return ''
