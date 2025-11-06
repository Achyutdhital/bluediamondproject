from django import forms
from .models import Enquiry, Services, TrainingCourse


class EnquiryForm(forms.ModelForm):
    # Create a custom choice field that combines services and training courses
    enquiry_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="I'm interested in"
    )

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone_number", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name..", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "Email.."}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Mobile no..", "required": True}),
            "message": forms.Textarea(attrs={"placeholder": "Write message..", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build choices dynamically
        choices = [('', '--- Select Service or Course ---')]
        
        # Add services
        services = Services.objects.filter(is_active=True).order_by('name')
        if services:
            service_choices = [('service_' + str(s.id), f'Service: {s.name}') for s in services]
            choices.extend(service_choices)
        
        # Add training courses
        courses = TrainingCourse.objects.filter(is_active=True).order_by('title')
        if courses:
            course_choices = [('course_' + str(c.id), f'Training: {c.title}') for c in courses]
            choices.extend(course_choices)
        
        self.fields['enquiry_type'].choices = choices
        
        # Pre-select based on initial values if provided
        if self.initial.get('service'):
            service = self.initial['service']
            self.fields['enquiry_type'].initial = f'service_{service.id}'
        elif self.initial.get('training_course'):
            course = self.initial['training_course']
            self.fields['enquiry_type'].initial = f'course_{course.id}'

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number", "").strip()
        if not phone:
            raise forms.ValidationError("Please provide a phone number.")
        return phone

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Parse the enquiry_type to set service or training_course
        enquiry_type = self.cleaned_data.get('enquiry_type', '')
        if enquiry_type:
            if enquiry_type.startswith('service_'):
                service_id = int(enquiry_type.replace('service_', ''))
                instance.service_id = service_id
                instance.training_course = None
            elif enquiry_type.startswith('course_'):
                course_id = int(enquiry_type.replace('course_', ''))
                instance.training_course_id = course_id
                instance.service = None
        
        if commit:
            instance.save()
        return instance
