from django import forms
from django.forms import (
    TextInput,
    Textarea,
    ClearableFileInput,
    CheckboxInput,
    URLInput,
    DateTimeInput,
    Select,
)
from app.models import *
from ckeditor.widgets import CKEditorWidget


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        exclude = ['seo']  # Exclude SEO, handle separately
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Name'}),
            'short_description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'description': CKEditorWidget(),
            'feature_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'sort_order': TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-assigned'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If adding new service (no instance), show next number but allow editing
        if not self.instance.pk:
            from django.db.models import Max
            max_order = Services.objects.aggregate(Max('sort_order'))['sort_order__max']
            next_order = (max_order or 0) + 1
            self.fields['sort_order'].initial = next_order
            self.fields['sort_order'].help_text = f'Suggested: {next_order} (next available number). You can change this to any position.'
        else:
            self.fields['sort_order'].help_text = 'Change this number to reorder. Other items will shift automatically.'


class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        exclude = ['seo']  # Exclude SEO, handle separately
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'short_description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'description': CKEditorWidget(),
            'image': ClearableFileInput(attrs={'class': 'form-control'}),
            'duration': TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 months'}),
            'fee': TextInput(attrs={'class': 'form-control', 'placeholder': 'Course fee'}),
            'sort_order': TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-assigned'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If adding new course (no instance), show next number but allow editing
        if not self.instance.pk:
            from django.db.models import Max
            max_order = TrainingCourse.objects.aggregate(Max('sort_order'))['sort_order__max']
            next_order = (max_order or 0) + 1
            self.fields['sort_order'].initial = next_order
            self.fields['sort_order'].help_text = f'Suggested: {next_order} (next available number). You can change this to any position.'
        else:
            self.fields['sort_order'].help_text = 'Change this number to reorder. Other items will shift automatically.'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'


class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = '__all__'


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = '__all__'


class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = '__all__'


class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        fields = '__all__'


class HomeSectionForm(forms.ModelForm):
    class Meta:
        model = homesection
        fields = '__all__'


class AboutUsPageForm(forms.ModelForm):
    class Meta:
        model = AboutUsPage
        exclude = ['seo']  # Exclude SEO, handle separately
        widgets = {
            'page_title': TextInput(attrs={'class': 'form-control'}),
            'main_heading': TextInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(),
            'main_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'side_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'section_2_title': TextInput(attrs={'class': 'form-control'}),
            'section_2_content': CKEditorWidget(),
            'section_3_title': TextInput(attrs={'class': 'form-control'}),
            'section_3_content': CKEditorWidget(),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'


class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = '__all__'

class SeoMetadataForm(forms.ModelForm):
    class Meta:
        model = SEO
        fields = [
            'meta_title', 'meta_description', 'meta_keywords', 'focus_keyword',
            'og_title', 'og_description', 'og_image', 'og_type',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image',
            'canonical_url', 'robots', 'schema_type'
        ]
        widgets = {
            'meta_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO Title (50-60 chars)'}),
            'meta_description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Meta description (150-160 chars)'}),
            'meta_keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2, keyword3'}),
            'focus_keyword': TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary focus keyword'}),
            'og_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Open Graph title (optional, defaults to meta_title)'}),
            'og_description': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'OG description (optional)'}),
            'og_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'og_type': Select(attrs={'class': 'form-control'}),
            'twitter_card': Select(attrs={'class': 'form-control'}),
            'twitter_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter title (optional)'}),
            'twitter_description': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Twitter description (optional)'}),
            'twitter_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'canonical_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/page/ (optional)'}),
            'robots': TextInput(attrs={'class': 'form-control', 'placeholder': 'index, follow'}),
            'schema_type': Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional (not required)
        for field in self.fields.values():
            field.required = False


class PageSEOForm(forms.ModelForm):
    """Form for managing static page SEO (Homepage, Contact, etc.)"""
    class Meta:
        model = PageSEO
        fields = [
            'page', 'meta_title', 'meta_description', 'meta_keywords', 'focus_keyword',
            'og_title', 'og_description', 'og_image',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image',
            'canonical_url', 'robots', 'schema_type', 'is_active'
        ]
        widgets = {
            'page': Select(attrs={'class': 'form-control'}),
            'meta_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Page Title (50-60 chars)'}),
            'meta_description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Meta description (150-160 chars)'}),
            'meta_keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2, keyword3'}),
            'focus_keyword': TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary focus keyword'}),
            'og_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Open Graph title (optional)'}),
            'og_description': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'OG description (optional)'}),
            'og_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'twitter_card': Select(attrs={'class': 'form-control'}),
            'twitter_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter title (optional)'}),
            'twitter_description': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Twitter description (optional)'}),
            'twitter_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'canonical_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/page/ (optional)'}),
            'robots': TextInput(attrs={'class': 'form-control', 'placeholder': 'index, follow'}),
            'schema_type': Select(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional except 'page'
        for field_name, field in self.fields.items():
            if field_name != 'page':
                field.required = False

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__' 

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__' 

# New: Blog and Video forms
class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogPost
        exclude = ['seo']  # Exclude SEO, handle separately
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'excerpt': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short summary (optional)'}),
            'cover_image': ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_at': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'embed_url', 'is_active']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter video title'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (optional)'}),
            'video_file': ClearableFileInput(attrs={'class': 'form-control'}),
            'embed_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/embed/...'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DefaultSeoSettingsForm(forms.ModelForm):
    class Meta:
        model = DefaultSeoSettings
        fields = '__all__'
        widgets = {
            'site_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Blue Diamond Service Center'}),
            'default_title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Name - Professional Services'}),
            'default_description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Default meta description for your website'}),
            'default_keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2, keyword3'}),
            'default_og_image': ClearableFileInput(attrs={'class': 'form-control'}),
            
            # Analytics & Tracking
            'google_analytics_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'G-XXXXXXXXXX'}),
            'google_tag_manager_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'GTM-XXXXXXX'}),
            'google_search_console_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'google-site-verification=...'}),
            'bing_webmaster_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'msvalidate.01=...'}),
            
            # Social Media
            'facebook_app_id': TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'twitter_handle': TextInput(attrs={'class': 'form-control', 'placeholder': 'yourusername'}),
            'linkedin_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/company/yourcompany'}),
            'instagram_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourcompany'}),
            'youtube_url': URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/c/yourcompany'}),
            
            # Schema & SEO
            'schema_org_type': TextInput(attrs={'class': 'form-control', 'placeholder': 'LocalBusiness'}),
            'robots_txt_content': Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'User-agent: *\nDisallow: /dashboard/'}),
            
            # Business Info
            'business_phone': TextInput(attrs={'class': 'form-control', 'placeholder': '+977-1-1234567'}),
            'business_email': TextInput(attrs={'class': 'form-control', 'placeholder': 'info@bluediamond.com'}),
            'business_address': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Street Address, City, Country'}),
            
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

