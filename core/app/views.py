from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    Carousel,
    Services,
    TrainingCourse,
    Brand,
    Testimonial,
    FAQ,
    Feature,
    homesection,
    AboutUsPage,
    GalleryImage,
    Banner,
    CompanyDetails,
    PrivacyPolicy,
    TermsAndConditions,
)
from .forms import EnquiryForm


def get_common_context():
    """Get common context data for all views"""
    return {
        'nav_services': Services.objects.filter(is_active=True).order_by('name')[:6],
        'company': CompanyDetails.objects.first(),
    }


def index(request):
    # Handle enquiry submission
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['home_form_message'] = {'type': 'success', 'text': 'Thank you! We\'ll contact you shortly.'}
            return redirect('home')
        else:
            request.session['home_form_message'] = {'type': 'error', 'text': 'Please correct the errors below.'}
    else:
        form = EnquiryForm()
    
    # Get form-specific message
    form_message = request.session.pop('home_form_message', None)

    context = {
        'carousels': Carousel.objects.filter(is_active=True)[:10],
        'services': Services.objects.filter(is_active=True).order_by('name')[:6],
        'training_courses': TrainingCourse.objects.filter(is_active=True).order_by('title')[:4],
        'brands': Brand.objects.filter(is_active=True).order_by('sort_order', 'name')[:12],
        'testimonials': Testimonial.objects.filter(is_active=True)[:12],
        'faqs': FAQ.objects.filter(is_active=True).order_by('sort_order', 'id')[:12],
        'features': Feature.objects.filter(is_active=True).order_by('sort_order')[:3],
        'enquiry_form': form,
        'homesection': homesection.objects.first(),
        'form_message': form_message,
        **get_common_context(),
    }
    return render(request, 'app/index.html', context)


def about(request):
    """About Us page"""
    aboutus = AboutUsPage.objects.filter(is_active=True).first()
    banner = Banner.objects.filter(page_path='/about/', is_active=True).first()
    context = {
        'aboutus': aboutus,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/aboutus.html', context)


def gallery(request):
    """Gallery page with optional filtering by service and pagination"""
    service_slug = request.GET.get('service')
    images = GalleryImage.objects.filter(is_active=True).select_related('service')

    selected_service = None
    if service_slug:
        selected_service = Services.objects.filter(slug=service_slug, is_active=True).first()
        if selected_service:
            images = images.filter(service=selected_service)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(images, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    services = Services.objects.filter(is_active=True).order_by('name')
    banner = Banner.objects.filter(page_path='/gallery/', is_active=True).first()

    context = {
        'services': services,
        'images': page_obj.object_list,
        'page_obj': page_obj,
        'selected_service': selected_service,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/gallery.html', context)


def enquiry(request):
    """Enquiry page for services and training courses"""
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your enquiry! We will contact you shortly.')
            return redirect('enquiry')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EnquiryForm()

    banner = Banner.objects.filter(page_path='/enquiry/', is_active=True).first()
    context = {
        'form': form,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/enquiry.html', context)


def contact(request):
    """Contact us page with form and company information"""
    from .models import Contact
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        
        if name and phone_number:
            Contact.objects.create(
                name=name,
                email=email or '',
                phone_number=phone_number,
                message=message or ''
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    banner = Banner.objects.filter(page_path='/contact/', is_active=True).first()
    context = {
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/contact.html', context)


def services(request):
    """Services page displaying all active services"""
    services = Services.objects.filter(is_active=True).order_by('name')
    banner = Banner.objects.filter(page_path='/services/', is_active=True).first()
    
    context = {
        'services': services,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/services.html', context)


def service_detail(request, slug):
    """Service detail page"""
    from django.shortcuts import get_object_or_404
    
    service = get_object_or_404(Services, slug=slug, is_active=True)
    other_services = Services.objects.filter(is_active=True).exclude(id=service.id).order_by('name')[:5]
    related_services = Services.objects.filter(is_active=True).exclude(id=service.id).order_by('?')[:3]
    
    context = {
        'service': service,
        'other_services': other_services,
        'related_services': related_services,
        **get_common_context(),
    }
    return render(request, 'app/service_detail.html', context)


def privacy_policy(request):
    """Privacy Policy page"""
    privacy = PrivacyPolicy.objects.filter(is_active=True).first()
    banner = Banner.objects.filter(page_path='/privacy-policy/', is_active=True).first()
    context = {
        'privacy': privacy,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/privacy_policy.html', context)


def terms_and_conditions(request):
    """Terms and Conditions page"""
    terms = TermsAndConditions.objects.filter(is_active=True).first()
    banner = Banner.objects.filter(page_path='/terms-and-conditions/', is_active=True).first()
    context = {
        'terms': terms,
        'banner': banner,
        **get_common_context(),
    }
    return render(request, 'app/terms_and_conditions.html', context)