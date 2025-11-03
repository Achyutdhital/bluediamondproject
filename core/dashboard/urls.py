from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
	# Auth
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),

	# Dashboard home
	path('', views.DashboardView.as_view(), name='dashboard'),

	# Services
	path('services/', views.ServicesListView.as_view(), name='services_list'),
	path('services/add/', views.ServiceAddEditView.as_view(), name='service_add'),
	path('services/<int:pk>/edit/', views.ServiceAddEditView.as_view(), name='service_edit'),
	path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

	# Training Courses
	path('training-courses/', views.TrainingCourseListView.as_view(), name='training_courses_list'),
	path('training-courses/add/', views.TrainingCourseAddEditView.as_view(), name='training_course_add'),
	path('training-courses/<int:pk>/edit/', views.TrainingCourseAddEditView.as_view(), name='training_course_edit'),
	path('training-courses/<int:pk>/delete/', views.TrainingCourseDeleteView.as_view(), name='training_course_delete'),

	# Brands
	path('brands/', views.BrandListView.as_view(), name='brands_list'),
	path('brands/add/', views.BrandAddEditView.as_view(), name='brand_add'),
	path('brands/<int:pk>/edit/', views.BrandAddEditView.as_view(), name='brand_edit'),
	path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),

	# Testimonials
	path('testimonials/', views.TestimonialListView.as_view(), name='testimonials_list'),
	path('testimonials/add/', views.TestimonialAddEditView.as_view(), name='testimonial_add'),
	path('testimonials/<int:pk>/edit/', views.TestimonialAddEditView.as_view(), name='testimonial_edit'),
	path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),

	# FAQs
	path('faqs/', views.FAQListView.as_view(), name='faqs_list'),
	path('faqs/add/', views.FAQAddEditView.as_view(), name='faq_add'),
	path('faqs/<int:pk>/edit/', views.FAQAddEditView.as_view(), name='faq_edit'),
	path('faqs/<int:pk>/delete/', views.FAQDeleteView.as_view(), name='faq_delete'),

	# Gallery
	path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
	path('gallery/add/', views.GalleryAddEditView.as_view(), name='gallery_add'),
	path('gallery/<int:pk>/edit/', views.GalleryAddEditView.as_view(), name='gallery_edit'),
	path('gallery/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),

	# Features
	path('features/', views.FeatureListView.as_view(), name='features_list'),
	path('features/add/', views.FeatureAddEditView.as_view(), name='feature_add'),
	path('features/<int:pk>/edit/', views.FeatureAddEditView.as_view(), name='feature_edit'),
	path('features/<int:pk>/delete/', views.FeatureDeleteView.as_view(), name='feature_delete'),

	# Carousel
	path('carousels/', views.CarouselListView.as_view(), name='carousels_list'),
	path('carousels/add/', views.CarouselAddEditView.as_view(), name='carousel_add'),
	path('carousels/<int:pk>/edit/', views.CarouselAddEditView.as_view(), name='carousel_edit'),
	path('carousels/<int:pk>/delete/', views.CarouselDeleteView.as_view(), name='carousel_delete'),

	# Banners
	path('banners/', views.BannerListView.as_view(), name='banners_list'),
	path('banners/add/', views.BannerAddEditView.as_view(), name='banner_add'),
	path('banners/<int:pk>/edit/', views.BannerAddEditView.as_view(), name='banner_edit'),
	path('banners/<int:pk>/delete/', views.BannerDeleteView.as_view(), name='banner_delete'),

	# Company / Home / About
	path('company-details/', views.CompanyDetailsEditView.as_view(), name='company_details_edit'),
	path('home-section/', views.HomeSectionEditView.as_view(), name='home_section_edit'),
	path('about-us/', views.AboutUsPageEditView.as_view(), name='about_us_page_edit'),

	# Policy pages
	path('privacy-policy/', views.PrivacyPolicyEditView.as_view(), name='privacy_policy_edit'),
	path('terms-conditions/', views.TermsConditionsEditView.as_view(), name='terms_conditions_edit'),

	# SEO
	path('seo-settings/', views.DefaultSeoSettingsEditView.as_view(), name='default_seo_settings_edit'),
	path('seo-metadata/', views.SeoMetadataListView.as_view(), name='seo_metadata_list'),
	path('seo-metadata/add/', views.SeoMetadataAddEditView.as_view(), name='seo_metadata_add'),
	path('seo-metadata/<int:pk>/edit/', views.SeoMetadataAddEditView.as_view(), name='seo_metadata_edit'),
	path('seo-metadata/<int:pk>/delete/', views.SeoMetadataDeleteView.as_view(), name='seo_metadata_delete'),
	
	# Page SEO (Homepage, Contact, Lists, etc.)
	path('page-seo/', views.PageSEOListView.as_view(), name='page_seo_list'),
	path('page-seo/add/', views.PageSEOAddEditView.as_view(), name='page_seo_add'),
	path('page-seo/<int:pk>/edit/', views.PageSEOAddEditView.as_view(), name='page_seo_edit'),
	path('page-seo/<int:pk>/delete/', views.PageSEODeleteView.as_view(), name='page_seo_delete'),

	# Enquiries
	path('enquiries/', views.EnquiryListView.as_view(), name='enquiries_list'),
	path('enquiries/<int:pk>/', views.EnquiryDetailView.as_view(), name='enquiry_detail'),
	path('enquiries/<int:pk>/update-status/', views.EnquiryUpdateStatusView.as_view(), name='enquiry_update_status'),

	# Contacts
	path('contacts/', views.ContactListView.as_view(), name='contacts_list'),
	path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
	path('contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),

	# Blog
	path('blogs/', views.BlogListView.as_view(), name='blogs_list'),
	path('blogs/add/', views.BlogAddEditView.as_view(), name='blog_add'),
	path('blogs/<int:pk>/edit/', views.BlogAddEditView.as_view(), name='blog_edit'),
	path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),

	# Videos
	path('videos/', views.VideoListView.as_view(), name='videos_list'),
	path('videos/add/', views.VideoAddEditView.as_view(), name='video_add'),
	path('videos/<int:pk>/edit/', views.VideoAddEditView.as_view(), name='video_edit'),
	path('videos/<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),
]

