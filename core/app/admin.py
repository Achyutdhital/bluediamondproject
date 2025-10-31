from django.contrib import admin
from . import models


class SeoMetadataInline(admin.StackedInline):
	model = models.SeoMetadata
	extra = 0
	max_num = 1
	fields = ('title', 'description', 'keywords')
	verbose_name = "SEO Metadata"
	verbose_name_plural = "SEO Metadata"


@admin.register(models.Services)
class ServicesAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
	list_filter = ("is_active",)
	search_fields = ("name", "short_description")
	fieldsets = (
		('Service Information', {
			'fields': ('name', 'short_description', 'description', 'feature_image', 'is_active')
		}),
		('SEO', {
			'fields': ('seo_metadata',),
			'classes': ('collapse',)
		}),
	)


@admin.register(models.TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
	list_display = ("title", "duration", "fee", "is_active")
	list_filter = ("is_active",)
	search_fields = ("title", "short_description")


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


@admin.register(models.SeoMetadata)
class SeoMetadataAdmin(admin.ModelAdmin):
	list_display = ("title", "content_type", "object_id")
	search_fields = ("title", "description", "keywords")


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
