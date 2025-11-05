from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q

from app.models import (
	Services,
	TrainingCourse,
	Brand,
	Testimonial,
	FAQ,
	GalleryImage,
	Feature,
	Carousel,

	CompanyDetails,
	homesection,
	AboutUsPage,
	PrivacyPolicy,
	TermsAndConditions,
	SEO,
	PageSEO,
	DefaultSeoSettings,
	Enquiry,
	Contact,
    BlogPost,
    Video,
)

from .forms import (
	ServiceForm,
	TrainingCourseForm,
	BrandForm,
	TestimonialForm,
	FAQForm,
	GalleryForm,
	FeatureForm,
	CarouselForm,

	CompanyDetailsForm,
	HomeSectionForm,
	AboutUsPageForm,
	PrivacyPolicyForm,
	TermsAndConditionsForm,
	SeoMetadataForm,
	PageSEOForm,
	DefaultSeoSettingsForm,
	EnquiryForm as DashboardEnquiryForm,  # not used for create here, but kept for completeness
	ContactForm as DashboardContactForm,  # not used
	BlogPostForm,
	VideoForm,
)


# Authentication Views
class LoginView(View):
	template_name = 'dashboard/login.html'

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('dashboard:dashboard')
		form = AuthenticationForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard:dashboard')
		messages.error(request, 'Invalid username or password.')
		return render(request, self.template_name, {'form': form})


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('dashboard:login')


class ChangePasswordView(LoginRequiredMixin, View):
	template_name = 'dashboard/change_password.html'

	def get(self, request):
		form = PasswordChangeForm(user=request.user)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Password changed successfully.')
			return redirect('dashboard:dashboard')
		messages.error(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form})


# Dashboard Home
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Counts
		context['services_count'] = Services.objects.count()
		context['training_courses_count'] = TrainingCourse.objects.count()
		context['gallery_count'] = GalleryImage.objects.count()
		context['testimonials_count'] = Testimonial.objects.count()
		context['enquiries_pending'] = Enquiry.objects.filter(status=Enquiry.NEW).count()
		context['contacts_count'] = Contact.objects.count()
		context['brands_count'] = Brand.objects.count()
		context['faqs_count'] = FAQ.objects.count()
		# Recents
		context['recent_enquiries'] = Enquiry.objects.order_by('-created_at')[:5]
		context['recent_contacts'] = Contact.objects.order_by('-created_at')[:5]
		context['recent_testimonials'] = Testimonial.objects.order_by('-created_at')[:5]
		return context


# Generic patterns for CRUD-like flows using explicit forms and templates

class ServicesListView(LoginRequiredMixin, ListView):
	model = Services
	template_name = 'dashboard/services_list.html'
	context_object_name = 'services'


class ServiceAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/service_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Services, pk=pk) if pk else None
		form = ServiceForm(instance=instance)
		seo_form = SeoMetadataForm(instance=instance.seo if instance and instance.seo else None)
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Services, pk=pk) if pk else None
		form = ServiceForm(request.POST, request.FILES, instance=instance)
		seo_form = SeoMetadataForm(request.POST, request.FILES, instance=instance.seo if instance and instance.seo else None)
		
		if form.is_valid():
			# Save service without committing to database yet
			service = form.save(commit=False)
			
			# Handle SEO separately if ANY field is provided
			has_seo_data = any([
				seo_form.data.get('meta_title'),
				seo_form.data.get('meta_description'),
				seo_form.data.get('meta_keywords'),
				seo_form.data.get('focus_keyword'),
			])
			
			if has_seo_data:
				if seo_form.is_valid():
					seo = seo_form.save()
					service.seo = seo
				else:
					# Show SEO form errors - display actual errors for debugging
					for field, errors in seo_form.errors.items():
						for error in errors:
							messages.error(request, f'SEO {field}: {error}')
					return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})
			
			# Now save the service (will auto-generate SEO only if seo_id is still None)
			service.save()
			
			messages.success(request, 'Service saved successfully.' if not instance else 'Service updated successfully.')
			return redirect('dashboard:services_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})


class ServiceDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Services, pk=pk)
		instance.delete()
		messages.success(request, 'Service deleted successfully.')
		return redirect('dashboard:services_list')


class TrainingCourseListView(LoginRequiredMixin, ListView):
	model = TrainingCourse
	template_name = 'dashboard/training_courses_list.html'
	context_object_name = 'courses'


class TrainingCourseAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/training_course_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(TrainingCourse, pk=pk) if pk else None
		form = TrainingCourseForm(instance=instance)
		seo_form = SeoMetadataForm(instance=instance.seo if instance and instance.seo else None)
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(TrainingCourse, pk=pk) if pk else None
		form = TrainingCourseForm(request.POST, request.FILES, instance=instance)
		seo_form = SeoMetadataForm(request.POST, request.FILES, instance=instance.seo if instance and instance.seo else None)
		
		if form.is_valid():
			# Save course without committing to database yet
			course = form.save(commit=False)
			
			# Handle SEO separately if ANY field is provided
			has_seo_data = any([
				seo_form.data.get('meta_title'),
				seo_form.data.get('meta_description'),
				seo_form.data.get('meta_keywords'),
				seo_form.data.get('focus_keyword'),
			])
			
			if has_seo_data:
				if seo_form.is_valid():
					seo = seo_form.save()
					course.seo = seo
				else:
					# Show SEO form errors - display actual errors for debugging
					for field, errors in seo_form.errors.items():
						for error in errors:
							messages.error(request, f'SEO {field}: {error}')
					return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})
			
			# Now save the course (will auto-generate SEO only if seo_id is still None)
			course.save()
			
			messages.success(request, 'Training course saved successfully.' if not instance else 'Training course updated successfully.')
			return redirect('dashboard:training_courses_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})


class TrainingCourseDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(TrainingCourse, pk=pk)
		instance.delete()
		messages.success(request, 'Training course deleted successfully.')
		return redirect('dashboard:training_courses_list')


class BrandListView(LoginRequiredMixin, ListView):
	model = Brand
	template_name = 'dashboard/brands_list.html'
	context_object_name = 'brands'


class BrandAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/brand_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Brand, pk=pk) if pk else None
		form = BrandForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Brand, pk=pk) if pk else None
		form = BrandForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Brand saved successfully.' if not instance else 'Brand updated successfully.')
			return redirect('dashboard:brands_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class BrandDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Brand, pk=pk)
		instance.delete()
		messages.success(request, 'Brand deleted successfully.')
		return redirect('dashboard:brands_list')


class TestimonialListView(LoginRequiredMixin, ListView):
	model = Testimonial
	template_name = 'dashboard/testimonials_list.html'
	context_object_name = 'testimonials'


class TestimonialAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/testimonial_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Testimonial, pk=pk) if pk else None
		form = TestimonialForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Testimonial, pk=pk) if pk else None
		form = TestimonialForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Testimonial saved successfully.' if not instance else 'Testimonial updated successfully.')
			return redirect('dashboard:testimonials_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class TestimonialDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Testimonial, pk=pk)
		instance.delete()
		messages.success(request, 'Testimonial deleted successfully.')
		return redirect('dashboard:testimonials_list')


class FAQListView(LoginRequiredMixin, ListView):
	model = FAQ
	template_name = 'dashboard/faqs_list.html'
	context_object_name = 'faqs'


class FAQAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/faq_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(FAQ, pk=pk) if pk else None
		form = FAQForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(FAQ, pk=pk) if pk else None
		form = FAQForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'FAQ saved successfully.' if not instance else 'FAQ updated successfully.')
			return redirect('dashboard:faqs_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class FAQDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(FAQ, pk=pk)
		instance.delete()
		messages.success(request, 'FAQ deleted successfully.')
		return redirect('dashboard:faqs_list')


class GalleryListView(LoginRequiredMixin, ListView):
	model = GalleryImage
	template_name = 'dashboard/gallery_list.html'
	context_object_name = 'images'
	paginate_by = 12

	def get_queryset(self):
		queryset = GalleryImage.objects.all().order_by('-created_at')
		service_id = self.request.GET.get('service')
		if service_id:
			queryset = queryset.filter(service_id=service_id)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['services'] = Services.objects.filter(is_active=True)
		context['selected_service'] = self.request.GET.get('service', '')
		return context


class GalleryAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/gallery_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(GalleryImage, pk=pk) if pk else None
		form = GalleryForm(instance=instance)
		context = {
			'form': form,
			'gallery_image': instance,
			'services': Services.objects.filter(is_active=True)
		}
		return render(request, self.template_name, context)

	def post(self, request, pk=None):
		instance = get_object_or_404(GalleryImage, pk=pk) if pk else None
		form = GalleryForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Gallery image saved successfully.' if not instance else 'Gallery image updated successfully.')
			return redirect('dashboard:gallery_list')
		messages.warning(request, 'Please correct the errors below.')
		context = {
			'form': form,
			'gallery_image': instance,
			'services': Services.objects.filter(is_active=True)
		}
		return render(request, self.template_name, context)


class GalleryDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(GalleryImage, pk=pk)
		instance.delete()
		messages.success(request, 'Gallery image deleted successfully.')
		return redirect('dashboard:gallery_list')


class FeatureListView(LoginRequiredMixin, ListView):
	model = Feature
	template_name = 'dashboard/features_list.html'
	context_object_name = 'features'


class FeatureAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/feature_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Feature, pk=pk) if pk else None
		form = FeatureForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Feature, pk=pk) if pk else None
		form = FeatureForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Feature saved successfully.' if not instance else 'Feature updated successfully.')
			return redirect('dashboard:features_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class FeatureDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Feature, pk=pk)
		instance.delete()
		messages.success(request, 'Feature deleted successfully.')
		return redirect('dashboard:features_list')


class CarouselListView(LoginRequiredMixin, ListView):
	model = Carousel
	template_name = 'dashboard/carousel_list.html'
	context_object_name = 'carousels'


class CarouselAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/carousel_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Carousel, pk=pk) if pk else None
		form = CarouselForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Carousel, pk=pk) if pk else None
		form = CarouselForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Carousel saved successfully.' if not instance else 'Carousel updated successfully.')
			return redirect('dashboard:carousels_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class CarouselDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Carousel, pk=pk)
		instance.delete()
		messages.success(request, 'Carousel deleted successfully.')
		return redirect('dashboard:carousels_list')


# Singleton-like editors
class CompanyDetailsEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/company_details_edit.html'

	def get(self, request):
		instance = CompanyDetails.objects.first()
		form = CompanyDetailsForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request):
		instance = CompanyDetails.objects.first()
		form = CompanyDetailsForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Company details saved successfully.')
			return redirect('dashboard:company_details_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class HomeSectionEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/home_section_edit.html'

	def get(self, request):
		instance = homesection.objects.first()
		form = HomeSectionForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request):
		instance = homesection.objects.first()
		form = HomeSectionForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Home section saved successfully.')
			return redirect('dashboard:home_section_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class AboutUsPageEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/aboutus_add_edit.html'

	def get(self, request):
		instance = AboutUsPage.objects.first()
		form = AboutUsPageForm(instance=instance)
		# Initialize SEO form
		seo_form = SeoMetadataForm(instance=instance.seo if instance and instance.seo else None)
		return render(request, self.template_name, {
			'form': form,
			'instance': instance,
			'seo_form': seo_form
		})

	def post(self, request):
		instance = AboutUsPage.objects.first()
		form = AboutUsPageForm(request.POST, request.FILES, instance=instance)
		seo_form = SeoMetadataForm(
			request.POST,
			request.FILES,
			instance=instance.seo if instance and instance.seo else None
		)
		
		if form.is_valid():
			about_page = form.save()
			# Save SEO data only if user provided something meaningful
			if seo_form.is_valid() and (seo_form.cleaned_data.get('meta_title') or seo_form.cleaned_data.get('meta_description')):
				seo = seo_form.save()
				about_page.seo = seo
				about_page.save(update_fields=['seo'])
			messages.success(request, 'About Us page saved successfully.')
			return redirect('dashboard:about_us_page_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {
			'form': form,
			'instance': instance,
			'seo_form': seo_form
		})


class PrivacyPolicyEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/privacy_policy_add_edit.html'

	def get(self, request):
		instance = PrivacyPolicy.objects.first()
		form = PrivacyPolicyForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request):
		instance = PrivacyPolicy.objects.first()
		form = PrivacyPolicyForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Privacy Policy saved successfully.')
			return redirect('dashboard:privacy_policy_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class TermsConditionsEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/terms_and_conditions_add_edit.html'

	def get(self, request):
		instance = TermsAndConditions.objects.first()
		form = TermsAndConditionsForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request):
		instance = TermsAndConditions.objects.first()
		form = TermsAndConditionsForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Terms and Conditions saved successfully.')
			return redirect('dashboard:terms_conditions_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


# SEO Metadata
class SeoMetadataListView(LoginRequiredMixin, ListView):
	model = SEO
	template_name = 'dashboard/seo_metadata_list.html'
	context_object_name = 'seo_metadata'


class SeoMetadataAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/seo_metadata_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(SEO, pk=pk) if pk else None
		form = SeoMetadataForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(SEO, pk=pk) if pk else None
		form = SeoMetadataForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'SEO metadata saved successfully.' if not instance else 'SEO metadata updated successfully.')
			return redirect('dashboard:seo_metadata_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class SeoMetadataDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(SEO, pk=pk)
		instance.delete()
		messages.success(request, 'SEO metadata deleted successfully.')
		return redirect('dashboard:seo_metadata_list')


# Enquiries
class EnquiryListView(LoginRequiredMixin, View):
	template_name = 'dashboard/enquiry_list.html'

	def get(self, request):
		status = request.GET.get('status', '')
		search = request.GET.get('search', '')
		qs = Enquiry.objects.all().order_by('-created_at')
		if status:
			qs = qs.filter(status=status)
		if search:
			qs = qs.filter(
				Q(name__icontains=search)
				| Q(email__icontains=search)
				| Q(phone_number__icontains=search)
			)
		paginator = Paginator(qs, 10)
		page_number = request.GET.get('page')
		enquiries_page = paginator.get_page(page_number)
		context = {
			'enquiries': enquiries_page,
			'status': status,
			'search': search,
			'status_choices': Enquiry.STATUS_CHOICES,
		}
		return render(request, self.template_name, context)


class EnquiryDetailView(LoginRequiredMixin, View):
	template_name = 'dashboard/enquiry_detail.html'

	def get(self, request, pk):
		enquiry = get_object_or_404(Enquiry, pk=pk)
		return render(request, self.template_name, {'enquiry': enquiry})


class EnquiryUpdateStatusView(LoginRequiredMixin, View):
	def post(self, request, pk):
		enquiry = get_object_or_404(Enquiry, pk=pk)
		status = request.POST.get('status')
		if status in dict(Enquiry.STATUS_CHOICES):
			enquiry.status = status
			enquiry.save(update_fields=['status'])
			messages.success(request, 'Enquiry status updated.')
		else:
			messages.warning(request, 'Invalid status value.')
		# Redirect back to detail if referrer path contains detail, else to list
		try:
			ref = request.META.get('HTTP_REFERER', '')
			if ref and '/enquiries/' in ref and ref.rstrip('/').endswith(str(pk)):
				return redirect('dashboard:enquiry_detail', pk=pk)
		except Exception:
			pass
		return redirect('dashboard:enquiries_list')


# Contacts
class ContactListView(LoginRequiredMixin, ListView):
	model = Contact
	template_name = 'dashboard/contact_list.html'
	context_object_name = 'contacts'


class ContactDetailView(LoginRequiredMixin, View):
	template_name = 'dashboard/contact_detail.html'

	def get(self, request, pk):
		contact = get_object_or_404(Contact, pk=pk)
		return render(request, self.template_name, {'contact': contact})


class ContactDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		contact = get_object_or_404(Contact, pk=pk)
		contact.delete()
		messages.success(request, 'Contact deleted successfully.')
		return redirect('dashboard:contacts_list')


# Blog management
class BlogListView(LoginRequiredMixin, ListView):
	model = BlogPost
	template_name = 'dashboard/blog_list.html'
	context_object_name = 'blogs'


class BlogAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/blog_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(BlogPost, pk=pk) if pk else None
		form = BlogPostForm(instance=instance)
		seo_form = SeoMetadataForm(instance=instance.seo if instance and instance.seo else None)
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(BlogPost, pk=pk) if pk else None
		form = BlogPostForm(request.POST, request.FILES, instance=instance)
		seo_form = SeoMetadataForm(request.POST, request.FILES, instance=instance.seo if instance and instance.seo else None)
		
		if form.is_valid():
			# Save blog without committing to database yet
			blog = form.save(commit=False)
			
			# Handle SEO separately if ANY field is provided
			has_seo_data = any([
				seo_form.data.get('meta_title'),
				seo_form.data.get('meta_description'),
				seo_form.data.get('meta_keywords'),
				seo_form.data.get('focus_keyword'),
			])
			
			if has_seo_data:
				if seo_form.is_valid():
					seo = seo_form.save()
					blog.seo = seo
				else:
					# Show SEO form errors - display actual errors for debugging
					for field, errors in seo_form.errors.items():
						for error in errors:
							messages.error(request, f'SEO {field}: {error}')
					return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})
			
			# Now save the blog (will auto-generate SEO only if seo_id is still None)
			blog.save()
			
			messages.success(request, 'Blog saved successfully.' if not instance else 'Blog updated successfully.')
			return redirect('dashboard:blogs_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'seo_form': seo_form, 'instance': instance})


class BlogDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(BlogPost, pk=pk)
		instance.delete()
		messages.success(request, 'Blog deleted successfully.')
		return redirect('dashboard:blogs_list')


# Video management
class VideoListView(LoginRequiredMixin, ListView):
	model = Video
	template_name = 'dashboard/video_list.html'
	context_object_name = 'videos'


class VideoAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/video_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(Video, pk=pk) if pk else None
		form = VideoForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(Video, pk=pk) if pk else None
		form = VideoForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			obj = form.save()
			# Ensure only one active video at a time; when this one is active, deactivate others
			if obj.is_active:
				Video.objects.exclude(pk=obj.pk).update(is_active=False)
			messages.success(request, 'Video saved successfully.' if not instance else 'Video updated successfully.')
			return redirect('dashboard:videos_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class VideoDeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(Video, pk=pk)
		instance.delete()
		messages.success(request, 'Video deleted successfully.')
		return redirect('dashboard:videos_list')


# Default SEO Settings
class DefaultSeoSettingsEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/default_seo_settings_edit.html'

	def get(self, request):
		instance = DefaultSeoSettings.objects.first()
		form = DefaultSeoSettingsForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request):
		instance = DefaultSeoSettings.objects.first()
		form = DefaultSeoSettingsForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'SEO settings saved successfully.')
			return redirect('dashboard:default_seo_settings_edit')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


# Page SEO Management (Homepage, Contact, Services List, etc.)
class PageSEOListView(LoginRequiredMixin, ListView):
	model = PageSEO
	template_name = 'dashboard/page_seo_list.html'
	context_object_name = 'page_seos'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Show which pages don't have SEO yet
		existing_pages = PageSEO.objects.values_list('page', flat=True)
		all_pages = dict(PageSEO.PAGE_CHOICES)
		missing_pages = [(k, v) for k, v in all_pages.items() if k not in existing_pages]
		context['missing_pages'] = missing_pages
		return context


class PageSEOAddEditView(LoginRequiredMixin, View):
	template_name = 'dashboard/page_seo_add_edit.html'

	def get(self, request, pk=None):
		instance = get_object_or_404(PageSEO, pk=pk) if pk else None
		form = PageSEOForm(instance=instance)
		return render(request, self.template_name, {'form': form, 'instance': instance})

	def post(self, request, pk=None):
		instance = get_object_or_404(PageSEO, pk=pk) if pk else None
		form = PageSEOForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			messages.success(request, 'Page SEO saved successfully.' if not instance else 'Page SEO updated successfully.')
			return redirect('dashboard:page_seo_list')
		messages.warning(request, 'Please correct the errors below.')
		return render(request, self.template_name, {'form': form, 'instance': instance})


class PageSEODeleteView(LoginRequiredMixin, View):
	def post(self, request, pk):
		instance = get_object_or_404(PageSEO, pk=pk)
		instance.delete()
		messages.success(request, 'Page SEO deleted successfully.')
		return redirect('dashboard:page_seo_list')

