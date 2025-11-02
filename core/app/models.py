from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from datetime import timezone
from django.core.validators import FileExtensionValidator
from django.utils import timezone as dj_timezone



class SEO(models.Model):
    """
    Modern SEO model with comprehensive meta tags support.
    Supports Google, Facebook Open Graph, Twitter Cards, and Schema.org
    """
    # Basic Meta Tags
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text='SEO title (50-60 chars recommended)'
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text='Meta description (150-160 chars recommended)'
    )
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True,
        help_text='Comma-separated keywords (optional, less important for modern SEO)'
    )
    
    # Open Graph (Facebook, LinkedIn, etc.)
    og_title = models.CharField(
        max_length=60, 
        blank=True, 
        help_text='Open Graph title (defaults to meta_title if empty)'
    )
    og_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text='Open Graph description (defaults to meta_description if empty)'
    )
    og_image = models.ImageField(
        upload_to='seo/og_images/', 
        blank=True, 
        null=True, 
        help_text='Open Graph image - 1200x630px recommended'
    )
    og_type = models.CharField(
        max_length=20,
        default='website',
        help_text='Open Graph type (website, article, etc.)'
    )
    
    # Twitter Card
    twitter_card = models.CharField(
        max_length=20,
        default='summary_large_image',
        choices=[
            ('summary', 'Summary'),
            ('summary_large_image', 'Summary Large Image'),
            ('app', 'App'),
            ('player', 'Player'),
        ],
        help_text='Twitter card type'
    )
    twitter_title = models.CharField(
        max_length=60, 
        blank=True,
        help_text='Twitter title (defaults to meta_title if empty)'
    )
    twitter_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text='Twitter description (defaults to meta_description if empty)'
    )
    twitter_image = models.ImageField(
        upload_to='seo/twitter_images/', 
        blank=True, 
        null=True,
        help_text='Twitter image (defaults to og_image if empty) - 1200x628px'
    )
    
    # Advanced SEO
    canonical_url = models.URLField(
        blank=True,
        help_text='Canonical URL (leave empty to auto-generate)'
    )
    robots = models.CharField(
        max_length=100,
        default='index, follow',
        help_text='Robots meta tag (index, follow / noindex, nofollow)'
    )
    
    # Schema.org (JSON-LD)
    schema_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('Article', 'Article'),
            ('BlogPosting', 'Blog Posting'),
            ('Service', 'Service'),
            ('Course', 'Course'),
            ('Organization', 'Organization'),
            ('LocalBusiness', 'Local Business'),
            ('WebPage', 'Web Page'),
        ],
        help_text='Schema.org type for structured data'
    )
    
    # Focus Keyword
    focus_keyword = models.CharField(
        max_length=100,
        blank=True,
        help_text='Primary focus keyword for this page'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'

    def __str__(self):
        return f"SEO: {self.meta_title}"

    def get_og_title(self):
        """Return OG title or fallback to meta title"""
        return self.og_title or self.meta_title

    def get_og_description(self):
        """Return OG description or fallback to meta description"""
        return self.og_description or self.meta_description
    
    def get_twitter_title(self):
        """Return Twitter title or fallback to meta title"""
        return self.twitter_title or self.meta_title
    
    def get_twitter_description(self):
        """Return Twitter description or fallback to meta description"""
        return self.twitter_description or self.meta_description
    
    def get_twitter_image(self):
        """Return Twitter image or fallback to OG image"""
        return self.twitter_image or self.og_image


class DefaultSeoSettings(models.Model):
    """Default SEO settings for the website"""
    site_name = models.CharField(max_length=100, default='Blue Diamond Service Center')
    default_title = models.CharField(max_length=60, help_text='Default page title template')
    default_description = models.CharField(max_length=160, help_text='Default meta description')
    default_keywords = models.CharField(max_length=255, help_text='Default keywords')
    default_og_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text='Default Open Graph image')
    
    # Analytics & Tracking
    google_analytics_id = models.CharField(max_length=20, blank=True, help_text='Google Analytics tracking ID (GA4)')
    google_tag_manager_id = models.CharField(max_length=20, blank=True, help_text='Google Tag Manager ID')
    google_search_console_id = models.CharField(max_length=100, blank=True, help_text='Google Search Console verification code')
    bing_webmaster_id = models.CharField(max_length=100, blank=True, help_text='Bing Webmaster verification code')
    
    # Social Media
    facebook_app_id = models.CharField(max_length=20, blank=True, help_text='Facebook App ID')
    twitter_handle = models.CharField(max_length=50, blank=True, help_text='Twitter handle without @')
    linkedin_url = models.URLField(blank=True, help_text='LinkedIn company page URL')
    instagram_url = models.URLField(blank=True, help_text='Instagram profile URL')
    youtube_url = models.URLField(blank=True, help_text='YouTube channel URL')
    
    # Schema.org & SEO
    schema_org_type = models.CharField(max_length=50, default='LocalBusiness', help_text='Schema.org type')
    robots_txt_content = models.TextField(blank=True, help_text='Custom robots.txt content')
    
    # Contact Info for Schema
    business_phone = models.CharField(max_length=20, blank=True, help_text='Business phone for schema markup')
    business_email = models.EmailField(blank=True, help_text='Business email for schema markup')
    business_address = models.TextField(blank=True, help_text='Business address for schema markup')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Default SEO Settings'
        verbose_name_plural = 'Default SEO Settings'

    def save(self, *args, **kwargs):
        if DefaultSeoSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one Default SEO Settings entry is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SEO Settings - {self.site_name}"
    
    def get_robots_txt(self):
        """Get robots.txt content with defaults"""
        if self.robots_txt_content:
            return self.robots_txt_content
        return "User-agent: *\nDisallow: /dashboard/\nSitemap: /sitemap.xml"





class Services(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, blank=True, null=True)
    short_description = models.TextField('short_description', max_length=900)
    description = RichTextField('description')
    feature_image = models.ImageField(upload_to='Services/')  # Feature Image
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    seo = models.OneToOneField('SEO', on_delete=models.CASCADE, blank=True, null=True, related_name='service')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_seo_title(self):
        """Generate SEO-friendly title"""
        if self.seo:
            return self.seo.meta_title
        return f"{self.name} Service | Blue Diamond Service Center Nepal"

    def get_seo_description(self):
        """Generate SEO description"""
        if self.seo:
            return self.seo.meta_description
        return self.short_description[:160] + '...' if len(self.short_description) > 160 else self.short_description






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
    picture1 = models.ImageField(upload_to='home_images/')

    subtitle2 = models.CharField(max_length=255, default='Professional Appliance Services You Can Trust')
    subcontent2 = models.TextField(max_length=500)

    subtitle3 = models.CharField(max_length=255, default='Why Choose Us')
    subcontent3 = models.TextField(max_length=500)
    
    
    



class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    logo = models.ImageField(upload_to='companydetails/logos/')
    # card_image = models.ImageField(upload_to='companydetails/cards/', blank=True, null=True)
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
    

# New: Short marketing videos for homepage
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Either host file or use an embed URL (e.g., YouTube/Vimeo)
    video_file = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        help_text='Upload MP4/WebM/Ogg up to ~100MB (~5 min at 1080p).'
    )
    embed_url = models.URLField(blank=True, null=True, help_text='YouTube/Vimeo share link (optional).')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Ensure at least one source is provided
        if not self.video_file and not self.embed_url:
            raise ValidationError('Provide a video file or an embed URL.')
        # Basic file size guard (~100MB)
        f = self.video_file
        if f and hasattr(f, 'size') and f.size and f.size > 100 * 1024 * 1024:
            raise ValidationError('Video file is too large. Please keep under 100MB (~5 minutes).')

    def __str__(self):
        return self.title


# New: Blog posts
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True)
    excerpt = models.TextField(blank=True, help_text='Short summary shown in lists (optional).')
    content = RichTextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=dj_timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    seo = models.OneToOneField('SEO', on_delete=models.CASCADE, blank=True, null=True, related_name='blog_post')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', args=[self.slug])

    def get_seo_title(self):
        """Generate SEO-friendly title"""
        if self.seo:
            return self.seo.meta_title
        return f"{self.title} | Blue Diamond Service Center Blog"

    def get_seo_description(self):
        """Generate SEO description from excerpt or content"""
        if self.seo:
            return self.seo.meta_description
        if self.excerpt:
            return self.excerpt[:160]
        from django.utils.html import strip_tags
        content_text = strip_tags(self.content)
        return content_text[:160] + '...' if len(content_text) > 160 else content_text


class Carousel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='carousel_images')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Banner(models.Model):
    TYPE_GRADIENT = 'gradient'
    TYPE_SOLID = 'solid'
    TYPE_IMAGE = 'image'
    BANNER_TYPE_CHOICES = [
        (TYPE_GRADIENT, 'Gradient'),
        (TYPE_SOLID, 'Solid Color'),
        (TYPE_IMAGE, 'Background Image (Legacy)')
    ]

    title = models.CharField(
        max_length=255,
        help_text='Default title (can be overridden by page content)'
    )
    subtitle = models.CharField(
        max_length=500,
        blank=True,
        help_text='Optional subtitle or description'
    )
    page_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='e.g., /services/, /blog/, /about/'
    )
    banner_type = models.CharField(
        max_length=20,
        choices=BANNER_TYPE_CHOICES,
        default=TYPE_GRADIENT
    )
    # For gradient/solid banners
    primary_color = models.CharField(
        max_length=7,
        default='#1e3c72',
        help_text='Hex color code (e.g., #1e3c72)'
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#2a5298',
        help_text='For gradients - end color'
    )
    text_color = models.CharField(
        max_length=7,
        default='#ffffff',
        help_text='Title and breadcrumb text color'
    )
    height = models.IntegerField(
        default=280,
        help_text='Banner height in pixels'
    )
    # Legacy/background image option
    image = models.ImageField(
        upload_to='carousel_images',
        blank=True,
        null=True,
        help_text="Only for 'image' type banners"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page_path']

    def __str__(self):
        return self.title


class TrainingCourse(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True)
    short_description = models.TextField(max_length=500, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='training_courses/', blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    seo = models.OneToOneField('SEO', on_delete=models.CASCADE, blank=True, null=True, related_name='training_course')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_seo_title(self):
        """Generate SEO-friendly title"""
        if self.seo:
            return self.seo.meta_title
        return f"{self.title} Training Course | Blue Diamond Service Center"

    def get_seo_description(self):
        """Generate SEO description"""
        if self.seo:
            return self.seo.meta_description
        desc = self.short_description or self.description
        if desc:
            from django.utils.html import strip_tags
            clean_desc = strip_tags(desc)
            return clean_desc[:160] + '...' if len(clean_desc) > 160 else clean_desc
        return f"Learn {self.title} with professional training at Blue Diamond Service Center."


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
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
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
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
    image = models.ImageField(upload_to='gallery/')
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
    icon = models.ImageField(upload_to='features/', blank=True, null=True)
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
    main_image = models.ImageField(upload_to='aboutus/', blank=True, null=True, help_text='Main about us image')
    side_image = models.ImageField(upload_to='aboutus/', blank=True, null=True, help_text='Side/secondary image')
    
    # Additional content sections (optional)
    section_2_title = models.CharField(max_length=255, blank=True, help_text='Second section title (optional)')
    section_2_content = RichTextField(blank=True, help_text='Second section content (optional)')
    
    section_3_title = models.CharField(max_length=255, blank=True, help_text='Third section title (optional)')
    section_3_content = RichTextField(blank=True, help_text='Third section content (optional)')
    
    # SEO
    seo = models.OneToOneField('SEO', on_delete=models.CASCADE, blank=True, null=True, related_name='about_us_page')
    
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


