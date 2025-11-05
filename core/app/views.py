from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
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
    CompanyDetails,
    PrivacyPolicy,
    TermsAndConditions,
    BlogPost,
    Video,
)
from .forms import EnquiryForm
from .seo_utils import SEOHelper


def get_common_context():
    """Get common context data for all views"""
    return {
        'nav_services': Services.objects.filter(is_active=True).order_by('sort_order', 'name')[:6],
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
    
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='home')

    context = {
        'carousels': Carousel.objects.filter(is_active=True)[:10],
        'services': Services.objects.filter(is_active=True).order_by('sort_order', 'name')[:6],
        'training_courses': TrainingCourse.objects.filter(is_active=True).order_by('sort_order', 'title')[:4],
        'brands': Brand.objects.filter(is_active=True).order_by('sort_order', 'name')[:12],
        'testimonials': Testimonial.objects.filter(is_active=True)[:12],
        'faqs': FAQ.objects.filter(is_active=True).order_by('sort_order', 'id')[:12],
        'features': Feature.objects.filter(is_active=True).order_by('sort_order')[:3],
        'latest_blogs': BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3],
        'featured_video': Video.objects.filter(is_active=True).first(),
        'enquiry_form': form,
        'homesection': homesection.objects.first(),
        'form_message': form_message,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/index.html', context)


def blog_list(request):
    """Public blog listing page"""
    from django.core.paginator import Paginator
    posts_qs = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    paginator = Paginator(posts_qs, 20)  # ~10 rows per page on desktop (≈3 columns)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build a small window of page numbers around the current page to simplify template logic
    current = page_obj.number
    total = paginator.num_pages
    start = max(1, current - 2)
    end = min(total, current + 2)
    page_numbers = list(range(start, end + 1))
    show_first = 1 not in page_numbers
    show_last = total not in page_numbers


    recent_posts = posts_qs[:5]
    
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='blog', request=request)
    
    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'page_numbers': page_numbers,
        'show_first': show_first,
        'show_last': show_last,
        'total_pages': total,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/blog_list.html', context)


def blog_detail(request, slug):
    """Public blog detail page"""
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-published_at')[:5]
    # Previous/Next posts by published date
    prev_post = (
        BlogPost.objects.filter(is_published=True, published_at__lt=post.published_at)
        .order_by('-published_at')
        .first()
    )
    next_post = (
        BlogPost.objects.filter(is_published=True, published_at__gt=post.published_at)
        .order_by('published_at')
        .first()
    )
    
    # SEO data for blog post
    seo_data = SEOHelper.get_page_seo_data(
        obj=post,
        canonical_url=request.build_absolute_uri()
    )
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
        'prev_post': prev_post,
        'next_post': next_post,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/blog_detail.html', context)


def about(request):
    """About Us page"""
    aboutus = AboutUsPage.objects.filter(is_active=True).first()
    # SEO data - use about page's SEO if available
    seo_data = SEOHelper.get_page_seo_data(obj=aboutus, page_type='about', request=request)
    
    context = {
        'aboutus': aboutus,
        **get_common_context(),
        **seo_data,
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

    services = Services.objects.filter(is_active=True).order_by('sort_order', 'name')
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='gallery', request=request)

    context = {
        'services': services,
        'images': page_obj.object_list,
        'page_obj': page_obj,
        'selected_service': selected_service,
        **get_common_context(),
        **seo_data,
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

    # SEO data
    seo_data = SEOHelper.get_page_seo_data(
        page_type='default',
        request=request,
        meta_title='Enquiry - Blue Diamond Service Center',
        meta_description='Get in touch with us for appliance repair services or training course enquiries. Quick response and professional service guaranteed.',
        meta_keywords='enquiry, service request, training enquiry, contact form'
    )
    
    context = {
        'form': form,
        **get_common_context(),
        **seo_data,
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
    
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='contact', request=request)
    
    context = {
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/contact.html', context)


def services(request):
    """Services page displaying all active services"""
    services_qs = Services.objects.filter(is_active=True).order_by('sort_order', 'name')
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(services_qs, 30)  # ~10 rows per page on desktop (≈3 columns)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='services', request=request)
    
    # Build a small window of page numbers around the current page to simplify template logic
    current = page_obj.number
    total = paginator.num_pages
    start = max(1, current - 2)
    end = min(total, current + 2)
    page_numbers = list(range(start, end + 1))
    show_first = 1 not in page_numbers
    show_last = total not in page_numbers

    context = {
        'services': page_obj.object_list,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'show_first': show_first,
        'show_last': show_last,
        'total_pages': total,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/services.html', context)


def service_detail(request, slug):
    """Service detail page"""
    from django.shortcuts import get_object_or_404
    
    service = get_object_or_404(Services, slug=slug, is_active=True)
    other_services = Services.objects.filter(is_active=True).exclude(id=service.id).order_by('sort_order', 'name')[:5]
    related_services = Services.objects.filter(is_active=True).exclude(id=service.id).order_by('?')[:3]
    
    # SEO data for service
    seo_data = SEOHelper.get_page_seo_data(
        obj=service,
        canonical_url=request.build_absolute_uri()
    )
    
    context = {
        'service': service,
        'other_services': other_services,
        'related_services': related_services,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/service_detail.html', context)


def privacy_policy(request):
    """Privacy Policy page"""
    privacy = PrivacyPolicy.objects.filter(is_active=True).first()
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(
        page_type='default',
        request=request,
        meta_title='Privacy Policy - Blue Diamond Service Center',
        meta_description='Read our privacy policy to understand how we collect, use, and protect your personal information.',
        meta_keywords='privacy policy, data protection, privacy'
    )
    
    context = {
        'privacy': privacy,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/privacy_policy.html', context)


def terms_and_conditions(request):
    """Terms and Conditions page"""
    terms = TermsAndConditions.objects.filter(is_active=True).first()
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(
        page_type='default',
        request=request,
        meta_title='Terms and Conditions - Blue Diamond Service Center',
        meta_description='Read our terms and conditions for using our services and website.',
        meta_keywords='terms and conditions, terms of service, legal'
    )
    
    context = {
        'terms': terms,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/terms_and_conditions.html', context)


def training_courses(request):
    """Training courses page displaying all active courses"""
    courses_qs = TrainingCourse.objects.filter(is_active=True).order_by('sort_order', 'title')
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(courses_qs, 30)  # ~10 rows per page on desktop (≈3 columns)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # SEO data
    seo_data = SEOHelper.get_page_seo_data(page_type='training', request=request)
    
    context = {
        'courses': page_obj.object_list,
        'page_obj': page_obj,
        # Page window like blog list
        'page_numbers': list(range(max(1, page_obj.number - 2), min(page_obj.paginator.num_pages, page_obj.number + 2) + 1)),
        'show_first': 1 not in list(range(max(1, page_obj.number - 2), min(page_obj.paginator.num_pages, page_obj.number + 2) + 1)),
        'show_last': page_obj.paginator.num_pages not in list(range(max(1, page_obj.number - 2), min(page_obj.paginator.num_pages, page_obj.number + 2) + 1)),
        'total_pages': page_obj.paginator.num_pages,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/training_courses.html', context)


def training_course_detail(request, slug):
    """Training course detail page"""
    from django.shortcuts import get_object_or_404
    
    course = get_object_or_404(TrainingCourse, slug=slug, is_active=True)
    other_courses = TrainingCourse.objects.filter(is_active=True).exclude(id=course.id).order_by('sort_order', 'title')[:3]
    
    # SEO data for training course
    seo_data = SEOHelper.get_page_seo_data(
        obj=course,
        canonical_url=request.build_absolute_uri()
    )
    
    context = {
        'course': course,
        'other_courses': other_courses,
        **get_common_context(),
        **seo_data,
    }
    return render(request, 'app/training_course_detail.html', context)


def custom_404_view(request, exception):
    """Custom 404 error page"""
    context = {
        **get_common_context(),
    }
    return render(request, '404.html', context, status=404)