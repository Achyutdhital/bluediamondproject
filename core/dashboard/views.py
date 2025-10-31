# Copy this entire file content and replace the current views.py content

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from app.models import (
    Services, TrainingCourse, Brand, Testimonial, FAQ, GalleryImage,
    Enquiry, Contact, Feature, AboutUsPage, CompanyDetails, PrivacyPolicy,
    TermsAndConditions, Carousel, Banner, homesection, SeoMetadata
)


def staff_required(user):
    return user.is_staff


# ===========================
# Authentication Views
# ===========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'dashboard/login.html')


@login_required(login_url='/dashboard/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:login')


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/change_password.html', context)


# ===========================
# Dashboard Home
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def dashboard_index(request):
    # Get counts
    context = {
        'services_count': Services.objects.count(),
        'training_courses_count': TrainingCourse.objects.count(),
        'brands_count': Brand.objects.count(),
        'testimonials_count': Testimonial.objects.count(),
        'faqs_count': FAQ.objects.count(),
        'gallery_count': GalleryImage.objects.count(),
        'features_count': Feature.objects.count(),
        'carousels_count': Carousel.objects.count(),
        'banners_count': Banner.objects.count(),
        'enquiries_pending': Enquiry.objects.filter(status='new').count(),
        'enquiries_total': Enquiry.objects.count(),
        'contacts_count': Contact.objects.count(),
        
        # Recent items
        'recent_enquiries': Enquiry.objects.all().order_by('-created_at')[:5],
        'recent_contacts': Contact.objects.all().order_by('-created_at')[:5],
        'recent_testimonials': Testimonial.objects.all().order_by('-created_at')[:5],
    }
    
    # Get company info for context
    context['about'] = CompanyDetails.objects.first()
    
    return render(request, 'dashboard/index.html', context)


# ===========================
# Services CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def services_list(request):
    search = request.GET.get('search', '')
    services = Services.objects.all().order_by('-created_at')
    
    if search:
        services = services.filter(
            Q(name__icontains=search) | 
            Q(short_description__icontains=search)
        )
    
    paginator = Paginator(services, 20)
    page = request.GET.get('page')
    services_page = paginator.get_page(page)
    
    context = {
        'services': services_page,
        'search': search,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/services_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def service_add_edit(request, pk=None):
    service = get_object_or_404(Services, pk=pk) if pk else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        feature_image = request.FILES.get('feature_image')
        
        if service:
            service.name = name
            service.short_description = short_description
            service.description = description
            service.is_active = is_active
            if feature_image:
                service.feature_image = feature_image
            service.save()
            messages.success(request, 'Service updated successfully!')
        else:
            service = Services.objects.create(
                name=name,
                short_description=short_description,
                description=description,
                is_active=is_active,
                feature_image=feature_image
            )
            messages.success(request, 'Service created successfully!')
        
        return redirect('dashboard:services_list')
    
    context = {
        'service': service,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/service_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def service_delete(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('dashboard:services_list')


# ===========================
# Training Courses CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def training_courses_list(request):
    search = request.GET.get('search', '')
    courses = TrainingCourse.objects.all().order_by('-created_at')
    
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | 
            Q(short_description__icontains=search)
        )
    
    paginator = Paginator(courses, 20)
    page = request.GET.get('page')
    courses_page = paginator.get_page(page)
    
    context = {
        'courses': courses_page,
        'search': search,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/training_courses_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def training_course_add_edit(request, pk=None):
    course = get_object_or_404(TrainingCourse, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        fee = request.POST.get('fee')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if course:
            course.title = title
            course.short_description = short_description
            course.description = description
            course.duration = duration
            course.fee = fee if fee else None
            course.is_active = is_active
            if image:
                course.image = image
            course.save()
            messages.success(request, 'Training course updated successfully!')
        else:
            course = TrainingCourse.objects.create(
                title=title,
                short_description=short_description,
                description=description,
                duration=duration,
                fee=fee if fee else None,
                is_active=is_active,
                image=image
            )
            messages.success(request, 'Training course created successfully!')
        
        return redirect('dashboard:training_courses_list')
    
    context = {
        'course': course,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/training_course_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def training_course_delete(request, pk):
    course = get_object_or_404(TrainingCourse, pk=pk)
    course.delete()
    messages.success(request, 'Training course deleted successfully!')
    return redirect('dashboard:training_courses_list')


# ===========================
# Brands CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def brands_list(request):
    brands = Brand.objects.all().order_by('sort_order', 'name')
    context = {
        'brands': brands,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/brands_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def brand_add_edit(request, pk=None):
    brand = get_object_or_404(Brand, pk=pk) if pk else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        logo = request.FILES.get('logo')
        
        if brand:
            brand.name = name
            brand.website = website
            brand.sort_order = int(sort_order)
            brand.is_active = is_active
            if logo:
                brand.logo = logo
            brand.save()
            messages.success(request, 'Brand updated successfully!')
        else:
            brand = Brand.objects.create(
                name=name,
                website=website,
                sort_order=int(sort_order),
                is_active=is_active,
                logo=logo
            )
            messages.success(request, 'Brand created successfully!')
        
        return redirect('dashboard:brands_list')
    
    context = {
        'brand': brand,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/brand_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    brand.delete()
    messages.success(request, 'Brand deleted successfully!')
    return redirect('dashboard:brands_list')


# ===========================
# Testimonials CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def testimonials_list(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    
    paginator = Paginator(testimonials, 20)
    page = request.GET.get('page')
    testimonials_page = paginator.get_page(page)
    
    context = {
        'testimonials': testimonials_page,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/testimonials_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def testimonial_add_edit(request, pk=None):
    testimonial = get_object_or_404(Testimonial, pk=pk) if pk else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        message = request.POST.get('message')
        rating = request.POST.get('rating', 5)
        is_active = request.POST.get('is_active') == 'on'
        photo = request.FILES.get('photo')
        
        if testimonial:
            testimonial.name = name
            testimonial.location = location
            testimonial.message = message
            testimonial.rating = int(rating)
            testimonial.is_active = is_active
            if photo:
                testimonial.photo = photo
            testimonial.save()
            messages.success(request, 'Testimonial updated successfully!')
        else:
            testimonial = Testimonial.objects.create(
                name=name,
                location=location,
                message=message,
                rating=int(rating),
                is_active=is_active,
                photo=photo
            )
            messages.success(request, 'Testimonial created successfully!')
        
        return redirect('dashboard:testimonials_list')
    
    context = {
        'testimonial': testimonial,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/testimonial_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('dashboard:testimonials_list')


# ===========================
# FAQs CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def faqs_list(request):
    category = request.GET.get('category', '')
    faqs = FAQ.objects.all().order_by('sort_order', 'id')
    
    if category:
        faqs = faqs.filter(category=category)
    
    context = {
        'faqs': faqs,
        'category': category,
        'categories': FAQ.CATEGORY_CHOICES,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/faqs_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def faq_add_edit(request, pk=None):
    faq = get_object_or_404(FAQ, pk=pk) if pk else None
    
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = request.POST.get('category')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        if faq:
            faq.question = question
            faq.answer = answer
            faq.category = category
            faq.sort_order = int(sort_order)
            faq.is_active = is_active
            faq.save()
            messages.success(request, 'FAQ updated successfully!')
        else:
            faq = FAQ.objects.create(
                question=question,
                answer=answer,
                category=category,
                sort_order=int(sort_order),
                is_active=is_active
            )
            messages.success(request, 'FAQ created successfully!')
        
        return redirect('dashboard:faqs_list')
    
    context = {
        'faq': faq,
        'categories': FAQ.CATEGORY_CHOICES,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/faq_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, 'FAQ deleted successfully!')
    return redirect('dashboard:faqs_list')


# ===========================
# Gallery CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def gallery_list(request):
    service_id = request.GET.get('service', '')
    images = GalleryImage.objects.all().select_related('service').order_by('-created_at')
    
    if service_id:
        images = images.filter(service_id=service_id)
    
    paginator = Paginator(images, 24)
    page = request.GET.get('page')
    images_page = paginator.get_page(page)
    
    context = {
        'images': images_page,
        'services': Services.objects.filter(is_active=True),
        'selected_service': service_id,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/gallery_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def gallery_add_edit(request, pk=None):
    gallery_image = get_object_or_404(GalleryImage, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        service_id = request.POST.get('service')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if gallery_image:
            gallery_image.title = title
            gallery_image.service_id = service_id if service_id else None
            gallery_image.is_active = is_active
            if image:
                gallery_image.image = image
            gallery_image.save()
            messages.success(request, 'Gallery image updated successfully!')
        else:
            if not image:
                messages.error(request, 'Please upload an image.')
                return redirect('dashboard:gallery_add')
            
            gallery_image = GalleryImage.objects.create(
                title=title,
                service_id=service_id if service_id else None,
                is_active=is_active,
                image=image
            )
            messages.success(request, 'Gallery image created successfully!')
        
        return redirect('dashboard:gallery_list')
    
    context = {
        'gallery_image': gallery_image,
        'services': Services.objects.filter(is_active=True),
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/gallery_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def gallery_delete(request, pk):
    gallery_image = get_object_or_404(GalleryImage, pk=pk)
    gallery_image.delete()
    messages.success(request, 'Gallery image deleted successfully!')
    return redirect('dashboard:gallery_list')


# ===========================
# Features CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def features_list(request):
    features = Feature.objects.all().order_by('sort_order')
    context = {
        'features': features,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/features_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def feature_add_edit(request, pk=None):
    feature = get_object_or_404(Feature, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        icon = request.FILES.get('icon')
        
        if feature:
            feature.title = title
            feature.description = description
            feature.sort_order = int(sort_order)
            feature.is_active = is_active
            if icon:
                feature.icon = icon
            feature.save()
            messages.success(request, 'Feature updated successfully!')
        else:
            feature = Feature.objects.create(
                title=title,
                description=description,
                sort_order=int(sort_order),
                is_active=is_active,
                icon=icon
            )
            messages.success(request, 'Feature created successfully!')
        
        return redirect('dashboard:features_list')
    
    context = {
        'feature': feature,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/feature_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def feature_delete(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()
    messages.success(request, 'Feature deleted successfully!')
    return redirect('dashboard:features_list')


# ===========================
# Carousels CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def carousels_list(request):
    carousels = Carousel.objects.all().order_by('-id')
    context = {
        'carousels': carousels,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/carousel_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def carousel_add_edit(request, pk=None):
    carousel = get_object_or_404(Carousel, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if carousel:
            carousel.title = title
            carousel.description = description
            carousel.is_active = is_active
            if image:
                carousel.image = image
            carousel.save()
            messages.success(request, 'Carousel updated successfully!')
        else:
            if not image:
                messages.error(request, 'Please upload an image.')
                return redirect('dashboard:carousel_add')
            
            carousel = Carousel.objects.create(
                title=title,
                description=description,
                is_active=is_active,
                image=image
            )
            messages.success(request, 'Carousel created successfully!')
        
        return redirect('dashboard:carousels_list')
    
    context = {
        'carousel': carousel,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/carousel_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def carousel_delete(request, pk):
    carousel = get_object_or_404(Carousel, pk=pk)
    carousel.delete()
    messages.success(request, 'Carousel deleted successfully!')
    return redirect('dashboard:carousels_list')


# ===========================
# Banners CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def banners_list(request):
    banners = Banner.objects.all().order_by('-id')
    context = {
        'banners': banners,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/banner_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def banner_add_edit(request, pk=None):
    banner = get_object_or_404(Banner, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        page_path = request.POST.get('page_path')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if banner:
            banner.title = title
            banner.page_path = page_path
            banner.is_active = is_active
            if image:
                banner.image = image
            banner.save()
            messages.success(request, 'Banner updated successfully!')
        else:
            if not image:
                messages.error(request, 'Please upload an image.')
                return redirect('dashboard:banner_add')
            
            banner = Banner.objects.create(
                title=title,
                page_path=page_path,
                is_active=is_active,
                image=image
            )
            messages.success(request, 'Banner created successfully!')
        
        return redirect('dashboard:banners_list')
    
    context = {
        'banner': banner,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/banner_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    banner.delete()
    messages.success(request, 'Banner deleted successfully!')
    return redirect('dashboard:banners_list')


# ===========================
# Enquiries (Read-only)
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def enquiries_list(request):
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    enquiries = Enquiry.objects.all().select_related('service', 'training_course').order_by('-created_at')
    
    if status:
        enquiries = enquiries.filter(status=status)
    
    if search:
        enquiries = enquiries.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
    
    paginator = Paginator(enquiries, 20)
    page = request.GET.get('page')
    enquiries_page = paginator.get_page(page)
    
    context = {
        'enquiries': enquiries_page,
        'status': status,
        'search': search,
        'status_choices': Enquiry.STATUS_CHOICES,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/enquiry_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    context = {
        'enquiry': enquiry,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/enquiry_detail.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def enquiry_update_status(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['new', 'contacted', 'closed']:
            enquiry.status = status
            enquiry.save()
            messages.success(request, f'Enquiry status updated to {status}!')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('dashboard:enquiries_list')


# ===========================
# Contacts (Read-only)
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def contacts_list(request):
    search = request.GET.get('search', '')
    contacts = Contact.objects.all().order_by('-created_at')
    
    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
    
    paginator = Paginator(contacts, 20)
    page = request.GET.get('page')
    contacts_page = paginator.get_page(page)
    
    context = {
        'contacts': contacts_page,
        'search': search,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/contact_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    context = {
        'contact': contact,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/contact_detail.html', context)


# ===========================
# Singleton Pages
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def company_details_edit(request):
    company = CompanyDetails.objects.first()
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        description = request.POST.get('description')
        map_location = request.POST.get('map_location')
        facebook_url = request.POST.get('facebook_url')
        twitter_url = request.POST.get('twitter_url')
        instagram_url = request.POST.get('instagram_url')
        linkedin_url = request.POST.get('linkedin_url')
        logo = request.FILES.get('logo')
        
        if company:
            company.company_name = company_name
            company.address = address
            company.email = email
            company.phone_number = phone_number
            company.description = description
            company.map_location = map_location
            company.facebook_url = facebook_url
            company.twitter_url = twitter_url
            company.instagram_url = instagram_url
            company.linkedin_url = linkedin_url
            if logo:
                company.logo = logo
            company.save()
            messages.success(request, 'Company details updated successfully!')
        else:
            company = CompanyDetails.objects.create(
                company_name=company_name,
                address=address,
                email=email,
                phone_number=phone_number,
                description=description,
                map_location=map_location,
                facebook_url=facebook_url,
                twitter_url=twitter_url,
                instagram_url=instagram_url,
                linkedin_url=linkedin_url,
                logo=logo,
            )
            messages.success(request, 'Company details created successfully!')
        
        return redirect('dashboard:company_details_edit')
    
    context = {
        'company': company,
        'about': company
    }
    return render(request, 'dashboard/company_details_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def home_section_edit(request):
    home_section = homesection.objects.first()
    
    if request.method == 'POST':
        subtitle1 = request.POST.get('subtitle1')
        subcontent1 = request.POST.get('subcontent1')
        subtitle2 = request.POST.get('subtitle2')
        subcontent2 = request.POST.get('subcontent2')
        subtitle3 = request.POST.get('subtitle3')
        subcontent3 = request.POST.get('subcontent3')
        picture1 = request.FILES.get('picture1')
        
        if home_section:
            home_section.subtitle1 = subtitle1
            home_section.subcontent1 = subcontent1
            home_section.subtitle2 = subtitle2
            home_section.subcontent2 = subcontent2
            home_section.subtitle3 = subtitle3
            home_section.subcontent3 = subcontent3
            if picture1:
                home_section.picture1 = picture1
            home_section.save()
            messages.success(request, 'Home section updated successfully!')
        else:
            home_section = homesection.objects.create(
                subtitle1=subtitle1,
                subcontent1=subcontent1,
                subtitle2=subtitle2,
                subcontent2=subcontent2,
                subtitle3=subtitle3,
                subcontent3=subcontent3,
                picture1=picture1
            )
            messages.success(request, 'Home section created successfully!')
        
        return redirect('dashboard:home_section_edit')
    
    context = {
        'home_section': home_section,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/home_section_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def about_us_page_edit(request):
    about_page = AboutUsPage.objects.first()
    
    if request.method == 'POST':
        page_title = request.POST.get('page_title')
        main_heading = request.POST.get('main_heading')
        content = request.POST.get('content')
        section_2_title = request.POST.get('section_2_title')
        section_2_content = request.POST.get('section_2_content')
        section_3_title = request.POST.get('section_3_title')
        section_3_content = request.POST.get('section_3_content')
        is_active = request.POST.get('is_active') == 'on'
        main_image = request.FILES.get('main_image')
        side_image = request.FILES.get('side_image')
        
        if about_page:
            about_page.page_title = page_title
            about_page.main_heading = main_heading
            about_page.content = content
            about_page.section_2_title = section_2_title
            about_page.section_2_content = section_2_content
            about_page.section_3_title = section_3_title
            about_page.section_3_content = section_3_content
            about_page.is_active = is_active
            if main_image:
                about_page.main_image = main_image
            if side_image:
                about_page.side_image = side_image
            about_page.save()
            messages.success(request, 'About Us page updated successfully!')
        else:
            about_page = AboutUsPage.objects.create(
                page_title=page_title,
                main_heading=main_heading,
                content=content,
                section_2_title=section_2_title,
                section_2_content=section_2_content,
                section_3_title=section_3_title,
                section_3_content=section_3_content,
                is_active=is_active,
                main_image=main_image,
                side_image=side_image
            )
            messages.success(request, 'About Us page created successfully!')
        
        return redirect('dashboard:about_us_page_edit')
    
    context = {
        'about_page': about_page,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/aboutus_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def privacy_policy_edit(request):
    privacy = PrivacyPolicy.objects.first()
    
    if request.method == 'POST':
        page_title = request.POST.get('page_title')
        content = request.POST.get('content')
        is_active = request.POST.get('is_active') == 'on'
        
        if privacy:
            privacy.page_title = page_title
            privacy.content = content
            privacy.is_active = is_active
            privacy.save()
            messages.success(request, 'Privacy Policy updated successfully!')
        else:
            privacy = PrivacyPolicy.objects.create(
                page_title=page_title,
                content=content,
                is_active=is_active
            )
            messages.success(request, 'Privacy Policy created successfully!')
        
        return redirect('dashboard:privacy_policy_edit')
    
    context = {
        'privacy': privacy,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/privacy_policy_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def terms_conditions_edit(request):
    terms = TermsAndConditions.objects.first()
    
    if request.method == 'POST':
        page_title = request.POST.get('page_title')
        content = request.POST.get('content')
        is_active = request.POST.get('is_active') == 'on'
        
        if terms:
            terms.page_title = page_title
            terms.content = content
            terms.is_active = is_active
            terms.save()
            messages.success(request, 'Terms and Conditions updated successfully!')
        else:
            terms = TermsAndConditions.objects.create(
                page_title=page_title,
                content=content,
                is_active=is_active
            )
            messages.success(request, 'Terms and Conditions created successfully!')
        
        return redirect('dashboard:terms_conditions_edit')
    
    context = {
        'terms': terms,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/terms_and_conditions_add_edit.html', context)


# ===========================
# SEO Metadata CRUD
# ===========================

@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def seo_metadata_list(request):
    seo_list = SeoMetadata.objects.all().order_by('-id')
    
    paginator = Paginator(seo_list, 20)
    page = request.GET.get('page')
    seo_page = paginator.get_page(page)
    
    context = {
        'seo_list': seo_page,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/seo_metadata_list.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def seo_metadata_add_edit(request, pk=None):
    seo = get_object_or_404(SeoMetadata, pk=pk) if pk else None
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        keywords = request.POST.get('keywords')
        
        if seo:
            seo.title = title
            seo.description = description
            seo.keywords = keywords
            seo.save()
            messages.success(request, 'SEO Metadata updated successfully!')
        else:
            messages.error(request, 'SEO Metadata requires content_type and object_id. Please use admin panel.')
        
        return redirect('dashboard:seo_metadata_list')
    
    context = {
        'seo': seo,
        'about': CompanyDetails.objects.first()
    }
    return render(request, 'dashboard/seo_metadata_add_edit.html', context)


@login_required(login_url='/dashboard/login/')
@user_passes_test(staff_required)
def seo_metadata_delete(request, pk):
    seo = get_object_or_404(SeoMetadata, pk=pk)
    seo.delete()
    messages.success(request, 'SEO Metadata deleted successfully!')
    return redirect('dashboard:seo_metadata_list')
