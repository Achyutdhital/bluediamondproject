from .models import DefaultSeoSettings, CompanyDetails

def company_info(request):
    """
    Context processor to make company information available in all templates
    """
    try:
        company = CompanyDetails.objects.first()
    except CompanyDetails.DoesNotExist:
        company = None
    
    return {
        'company': company,
    }

def seo_context(request):
    """
    Context processor to make SEO settings available in all templates
    """
    try:
        default_seo = DefaultSeoSettings.objects.filter(is_active=True).first()
    except DefaultSeoSettings.DoesNotExist:
        default_seo = None
    
    try:
        company = CompanyDetails.objects.first()
    except CompanyDetails.DoesNotExist:
        company = None
    
    return {
        'default_seo': default_seo,
        'company': company,
    }