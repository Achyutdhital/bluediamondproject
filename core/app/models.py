from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from datetime import timezone



class SeoMetadata(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"SEO metadata for {self.content_object}"





class Services(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, blank=True, null=True)
    short_description = models.TextField('short_description', max_length=900)
    description = RichTextField('description')
    feature_image = models.ImageField(upload_to='media/Services/')  # Feature Image
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seo_metadata = models.ForeignKey(SeoMetadata, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

    def __str__(self):
        return self.name






class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Contact Information"


class homesection(models.Model):

    subtitle1 = models.CharField(max_length=255, default='Welcome to Blue Diamond Service Center')
    subcontent1 = models.TextField(max_length=900)
    picture1 = models.ImageField(upload_to='media/home_images/')

    subtitle2 = models.CharField(max_length=255, default='Professional Appliance Services You Can Trust')
    subcontent2 = models.TextField(max_length=500)

    subtitle3 = models.CharField(max_length=255, default='Why Choose Us')
    subcontent3 = models.TextField(max_length=500)
    
    
    



class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    logo = models.ImageField(upload_to='media/companydetails/logos/')
    # card_image = models.ImageField(upload_to='media/companydetails/cards/', blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    map_location = models.URLField(blank=True, null=True)  # or use a geolocation field like models.PointField()
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # Add more fields as needed

    def save(self, *args, **kwargs):
        if CompanyDetails.objects.exists() and not self.pk:
            raise ValidationError("Only one 'About Us' entry is allowed. You can only edit the existing entry.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
    


class Carousel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='media/carousel_images')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/carousel_images')
    page_path = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TrainingCourse(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True)
    short_description = models.TextField(max_length=500, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='media/training_courses/', blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='media/brands/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.ImageField(upload_to='media/testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class FAQ(models.Model):
    GENERAL = 'general'
    SERVICES = 'services'
    PRICING = 'pricing'
    TRAINING = 'training'
    CATEGORY_CHOICES = [
        (GENERAL, 'General'),
        (SERVICES, 'Services'),
        (PRICING, 'Pricing'),
        (TRAINING, 'Training'),
    ]

    question = models.CharField(max_length=255)
    answer = RichTextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=GENERAL)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.question


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/gallery/')
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, blank=True, null=True, related_name='gallery_images')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    NEW = 'new'
    CONTACTED = 'contacted'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (CLOSED, 'Closed'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, blank=True, null=True, related_name='enquiries')
    training_course = models.ForeignKey('TrainingCourse', on_delete=models.SET_NULL, blank=True, null=True, related_name='enquiries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Enquiry from {self.name}"


class Feature(models.Model):
    """Why Choose Us features/benefits"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='media/features/', blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class AboutUsPage(models.Model):
    """About Us page content with rich text"""
    page_title = models.CharField(max_length=255, default='About Us')
    main_heading = models.CharField(max_length=255, help_text='Main heading for the page')
    content = RichTextField(help_text='Main about us content (supports rich text formatting)')
    
    # Optional images
    main_image = models.ImageField(upload_to='media/aboutus/', blank=True, null=True, help_text='Main about us image')
    side_image = models.ImageField(upload_to='media/aboutus/', blank=True, null=True, help_text='Side/secondary image')
    
    # Additional content sections (optional)
    section_2_title = models.CharField(max_length=255, blank=True, help_text='Second section title (optional)')
    section_2_content = RichTextField(blank=True, help_text='Second section content (optional)')
    
    section_3_title = models.CharField(max_length=255, blank=True, help_text='Third section title (optional)')
    section_3_content = RichTextField(blank=True, help_text='Third section content (optional)')
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Us Page'
        verbose_name_plural = 'About Us Page'
    
    def save(self, *args, **kwargs):
        if AboutUsPage.objects.exists() and not self.pk:
            raise ValidationError("Only one About Us page is allowed. Please edit the existing one.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.page_title


class PrivacyPolicy(models.Model):
    """Privacy Policy page content"""
    page_title = models.CharField(max_length=255, default='Privacy Policy')
    content = RichTextField(help_text='Privacy policy content (supports rich text formatting)')
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policy'
    
    def save(self, *args, **kwargs):
        if PrivacyPolicy.objects.exists() and not self.pk:
            raise ValidationError("Only one Privacy Policy is allowed. Please edit the existing one.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.page_title


class TermsAndConditions(models.Model):
    """Terms and Conditions page content"""
    page_title = models.CharField(max_length=255, default='Terms and Conditions')
    content = RichTextField(help_text='Terms and conditions content (supports rich text formatting)')
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'
    
    def save(self, *args, **kwargs):
        if TermsAndConditions.objects.exists() and not self.pk:
            raise ValidationError("Only one Terms and Conditions page is allowed. Please edit the existing one.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.page_title


