from django.contrib import admin
from . import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'created_at')
	list_filter = ('is_active', 'created_at')
	search_fields = ('title', 'description')


@admin.register(models.SEO)
class SEOAdmin(admin.ModelAdmin):
	list_display = ("meta_title", "focus_keyword", "updated_at")
	list_filter = ("robots", "og_type", "schema_type", "updated_at")
	search_fields = ("meta_title", "meta_description", "meta_keywords", "focus_keyword")
	fieldsets = (
		('Basic SEO', {
			'fields': ('meta_title', 'meta_description', 'meta_keywords', 'focus_keyword')
		}),
		('Open Graph (Facebook, LinkedIn)', {
			'fields': ('og_title', 'og_description', 'og_image', 'og_type'),
			'classes': ('collapse',)
		}),
		('Twitter Card', {
			'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image'),
			'classes': ('collapse',)
		}),
		('Advanced', {
			'fields': ('canonical_url', 'robots', 'schema_type'),
			'classes': ('collapse',)
		}),
	)


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_published', 'published_at')
	list_filter = ('is_published', 'published_at')
	search_fields = ('title', 'content')
	readonly_fields = ('slug',)
	fieldsets = (
		('Blog Information', {
			'fields': ('title', 'slug', 'excerpt', 'content', 'cover_image', 'is_published', 'published_at')
		}),
	)


@admin.register(models.Services)
class ServicesAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
	list_filter = ("is_active",)
	search_fields = ("name", "short_description")
	readonly_fields = ('slug',)
	fieldsets = (
		('Service Information', {
			'fields': ('name', 'slug', 'short_description', 'description', 'feature_image', 'is_active')
		}),
	)


@admin.register(models.TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
	list_display = ("title", "duration", "fee", "is_active")
	list_filter = ("is_active",)
	search_fields = ("title", "description")
	readonly_fields = ('slug',)
	fieldsets = (
		('Course Information', {
			'fields': ('title', 'slug', 'short_description', 'description', 'image', 'duration', 'fee', 'is_active')
		}),
	)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ("name", "sort_order", "is_active")
	list_editable = ("sort_order", "is_active")
	search_fields = ("name",)


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("name", "location", "rating", "is_active", "created_at")
	list_filter = ("is_active", "rating")
	search_fields = ("name", "location", "message")


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
	list_display = ("question", "category", "sort_order", "is_active")
	list_editable = ("sort_order", "is_active")
	list_filter = ("category", "is_active")
	search_fields = ("question", "answer")


@admin.register(models.GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
	list_display = ("title", "service", "is_active", "created_at")
	list_filter = ("is_active", "service")
	search_fields = ("title",)


@admin.register(models.Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
	list_display = ("name", "phone_number", "service", "training_course", "status", "created_at")
	list_filter = ("status", "service", "training_course")
	search_fields = ("name", "email", "phone_number", "message")


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone_number", "created_at")
	list_filter = ("created_at",)
	search_fields = ("name", "email", "phone_number", "message")
	readonly_fields = ("name", "email", "phone_number", "message", "created_at")
	
	def has_add_permission(self, request):
		return False


@admin.register(models.homesection)
class homesectionAdmin(admin.ModelAdmin):
	list_display = ("subtitle1",)


@admin.register(models.CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
	list_display = ("company_name", "phone_number", "email")


@admin.register(models.Carousel)
class CarouselAdmin(admin.ModelAdmin):
	list_display = ("title", "is_active")
	list_filter = ("is_active",)


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
	list_display = ("title", "page_path", "is_active")
	list_filter = ("is_active",)


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
	list_display = ("title", "sort_order", "is_active")
	list_editable = ("sort_order", "is_active")
	search_fields = ("title", "description")
	list_filter = ("is_active",)


@admin.register(models.AboutUsPage)
class AboutUsPageAdmin(admin.ModelAdmin):
	list_display = ("page_title", "is_active", "updated_at")
	fieldsets = (
		('Page Title', {
			'fields': ('page_title', 'main_heading')
		}),
		('Main Content', {
			'fields': ('content', 'main_image', 'side_image')
		}),
		('Additional Sections (Optional)', {
			'fields': (
				'section_2_title', 'section_2_content',
				'section_3_title', 'section_3_content'
			),
			'classes': ('collapse',)
		}),
		('Settings', {
			'fields': ('is_active',)
		}),
	)
	
	def has_add_permission(self, request):
		# Only allow adding if no instance exists
		if models.AboutUsPage.objects.exists():
			return False
		return True


@admin.register(models.PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
	list_display = ("page_title", "is_active", "updated_at")
	fieldsets = (
		('Page Information', {
			'fields': ('page_title', 'content')
		}),
		('Settings', {
			'fields': ('is_active',)
		}),
	)
	
	def has_add_permission(self, request):
		if models.PrivacyPolicy.objects.exists():
			return False
		return True


@admin.register(models.TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
	list_display = ("page_title", "is_active", "updated_at")
	fieldsets = (
		('Page Information', {
			'fields': ('page_title', 'content')
		}),
		('Settings', {
			'fields': ('is_active',)
		}),
	)
	
	def has_add_permission(self, request):
		if models.TermsAndConditions.objects.exists():
			return False
		return True


@admin.register(models.DefaultSeoSettings)
class DefaultSeoSettingsAdmin(admin.ModelAdmin):
	list_display = ("site_name", "is_active", "updated_at")
	fieldsets = (
		('Site Information', {
			'fields': ('site_name', 'default_title', 'default_description', 'default_keywords', 'default_og_image')
		}),
		('Social Media Links', {
			'fields': ('facebook_app_id', 'twitter_handle', 'linkedin_url', 'instagram_url', 'youtube_url'),
			'classes': ('collapse',)
		}),
		('Analytics & Tracking', {
			'fields': ('google_analytics_id', 'google_tag_manager_id', 'google_search_console_id', 'bing_webmaster_id'),
			'classes': ('collapse',)
		}),
		('Schema.org & Business Info', {
			'fields': ('schema_org_type', 'business_phone', 'business_email', 'business_address'),
			'classes': ('collapse',)
		}),
		('Advanced', {
			'fields': ('robots_txt_content',),
			'classes': ('collapse',)
		}),
		('Settings', {
			'fields': ('is_active',)
		}),
	)
	
	def has_add_permission(self, request):
		if models.DefaultSeoSettings.objects.exists():
			return False
		return True


@admin.register(models.PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
	list_display = ('page', 'meta_title', 'is_active', 'updated_at')
	list_filter = ('is_active', 'page', 'schema_type')
	search_fields = ('meta_title', 'meta_description', 'focus_keyword')
	readonly_fields = ('created_at', 'updated_at')
	
	fieldsets = (
		('Page Selection', {
			'fields': ('page',),
			'description': 'Select the page you want to configure SEO for.'
		}),
		('Basic SEO', {
			'fields': ('meta_title', 'meta_description', 'meta_keywords', 'focus_keyword'),
			'description': 'Essential SEO fields for search engines.'
		}),
		('Open Graph (Facebook, LinkedIn)', {
			'fields': ('og_title', 'og_description', 'og_image'),
			'classes': ('collapse',),
			'description': 'Social media preview settings. Leave blank to use meta title/description.'
		}),
		('Twitter Card', {
			'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image'),
			'classes': ('collapse',),
			'description': 'Twitter-specific preview settings.'
		}),
		('Advanced SEO', {
			'fields': ('canonical_url', 'robots', 'schema_type'),
			'classes': ('collapse',),
		}),
		('Status', {
			'fields': ('is_active', 'created_at', 'updated_at'),
		}),
	)
	
	def has_delete_permission(self, request, obj=None):
		"""Allow deletion to recreate if needed"""
		return True


