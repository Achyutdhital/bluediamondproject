"""
URL configuration for dashboard.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Dashboard Home
    path('', views.dashboard_index, name='dashboard'),
    
    # Services
    path('services/', views.services_list, name='services_list'),
    path('services/add/', views.service_add_edit, name='service_add'),
    path('services/<int:pk>/edit/', views.service_add_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Training Courses
    path('training-courses/', views.training_courses_list, name='training_courses_list'),
    path('training-courses/add/', views.training_course_add_edit, name='training_course_add'),
    path('training-courses/<int:pk>/edit/', views.training_course_add_edit, name='training_course_edit'),
    path('training-courses/<int:pk>/delete/', views.training_course_delete, name='training_course_delete'),
    
    # Brands
    path('brands/', views.brands_list, name='brands_list'),
    path('brands/add/', views.brand_add_edit, name='brand_add'),
    path('brands/<int:pk>/edit/', views.brand_add_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete, name='brand_delete'),
    
    # Testimonials
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', views.testimonial_add_edit, name='testimonial_add'),
    path('testimonials/<int:pk>/edit/', views.testimonial_add_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),
    
    # FAQs
    path('faqs/', views.faqs_list, name='faqs_list'),
    path('faqs/add/', views.faq_add_edit, name='faq_add'),
    path('faqs/<int:pk>/edit/', views.faq_add_edit, name='faq_edit'),
    path('faqs/<int:pk>/delete/', views.faq_delete, name='faq_delete'),
    
    # Gallery
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/add/', views.gallery_add_edit, name='gallery_add'),
    path('gallery/<int:pk>/edit/', views.gallery_add_edit, name='gallery_edit'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # Features
    path('features/', views.features_list, name='features_list'),
    path('features/add/', views.feature_add_edit, name='feature_add'),
    path('features/<int:pk>/edit/', views.feature_add_edit, name='feature_edit'),
    path('features/<int:pk>/delete/', views.feature_delete, name='feature_delete'),
    
    # Carousels
    path('carousels/', views.carousels_list, name='carousels_list'),
    path('carousels/add/', views.carousel_add_edit, name='carousel_add'),
    path('carousels/<int:pk>/edit/', views.carousel_add_edit, name='carousel_edit'),
    path('carousels/<int:pk>/delete/', views.carousel_delete, name='carousel_delete'),
    
    # Banners
    path('banners/', views.banners_list, name='banners_list'),
    path('banners/add/', views.banner_add_edit, name='banner_add'),
    path('banners/<int:pk>/edit/', views.banner_add_edit, name='banner_edit'),
    path('banners/<int:pk>/delete/', views.banner_delete, name='banner_delete'),
    
    # Enquiries (Read-only)
    path('enquiries/', views.enquiries_list, name='enquiries_list'),
    path('enquiries/<int:pk>/', views.enquiry_detail, name='enquiry_detail'),
    path('enquiries/<int:pk>/update-status/', views.enquiry_update_status, name='enquiry_update_status'),
    
    # Contacts (Read-only)
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    
    # Singleton Pages
    path('company-details/', views.company_details_edit, name='company_details_edit'),
    path('home-section/', views.home_section_edit, name='home_section_edit'),
    path('about-us-page/', views.about_us_page_edit, name='about_us_page_edit'),
    path('privacy-policy/', views.privacy_policy_edit, name='privacy_policy_edit'),
    path('terms-conditions/', views.terms_conditions_edit, name='terms_conditions_edit'),
    
    # SEO Metadata
    path('seo-metadata/', views.seo_metadata_list, name='seo_metadata_list'),
    path('seo-metadata/add/', views.seo_metadata_add_edit, name='seo_metadata_add'),
    path('seo-metadata/<int:pk>/edit/', views.seo_metadata_add_edit, name='seo_metadata_edit'),
    path('seo-metadata/<int:pk>/delete/', views.seo_metadata_delete, name='seo_metadata_delete'),
]
