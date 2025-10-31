from .models import CompanyDetails, homesection, Services


def company_info(request):
    """
    Make company information, about content, and services available in all templates
    """
    try:
        company = CompanyDetails.objects.first()
    except CompanyDetails.DoesNotExist:
        company = None
    
    try:
        about = homesection.objects.first()
    except homesection.DoesNotExist:
        about = None
    
    # Get active services for navigation menu
    nav_services = Services.objects.filter(is_active=True).order_by('name')[:10]
    
    # Default SEO data
    default_seo = {
        'title': f"{company.company_name} - Professional Appliance Repair Services" if company else "Blue Diamond Service Center",
        'description': company.description[:160] if company and company.description else "Professional appliance repair services for AC, refrigerator, washing machine, geyser, and more. Expert CTVT certified technicians with genuine parts and full warranty.",
        'keywords': 'appliance repair, AC repair, refrigerator repair, washing machine repair, geyser repair, Nepal, Kathmandu'
    }
    
    return {
        'company': company,
        'about': about,
        'nav_services': nav_services,
        'default_seo': default_seo,
    }
