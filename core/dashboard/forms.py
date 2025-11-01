from django import forms
from app.models import*
from ckeditor.widgets import CKEditorWidget


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        fields = '__all__'


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


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
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
        fields = '__all__'


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
        model = SeoMetadata
        fields = '__all__'

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__' 

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__' 

