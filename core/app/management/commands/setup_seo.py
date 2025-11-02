from django.core.management.base import BaseCommand
from app.models import DefaultSeoSettings

class Command(BaseCommand):
    help = 'Set up default SEO settings for the website'

    def handle(self, *args, **options):
        # Create default SEO settings if they don't exist
        if not DefaultSeoSettings.objects.exists():
            default_seo = DefaultSeoSettings.objects.create(
                site_name='Blue Diamond Service Center',
                default_title='Blue Diamond Service Center - Professional Appliance Repair Services Nepal',
                default_description='Expert appliance repair services in Nepal. AC, refrigerator, washing machine, geyser repair with certified technicians and genuine parts.',
                default_keywords='appliance repair Nepal, AC repair Kathmandu, refrigerator repair, washing machine service, geyser installation, appliance training courses',
                google_analytics_id='',  # Add your GA4 ID here
                google_tag_manager_id='',  # Add your GTM ID here
                facebook_app_id='',
                twitter_handle='',
                schema_org_type='LocalBusiness',
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created default SEO settings: {default_seo.site_name}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Default SEO settings already exist.')
            )