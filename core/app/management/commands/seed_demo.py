from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
from pathlib import Path

from app.models import (
    CompanyDetails,
    homesection,
    Feature,
    Carousel,
    Banner,
    Brand,
    Services,
    GalleryImage,
    TrainingCourse,
    Testimonial,
    FAQ,
    AboutUsPage,
    PrivacyPolicy,
    TermsAndConditions,
    BlogPost,
    Video,
)


SMALL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90wS\xde"
    b"\x00\x00\x00\x06PLTE\xff\x00\x00\x00\xff\x00\x00\x00\x00\xff\xa7z=\xda\x00\x00\x00\x19tEXtSoftware\x00Python\x20seed_demo\x9c\xce\x1d\n"
    b"\x00\x00\x00CIDAT(\x91c`\xa0\x1d\xf8\xff\x9f\x81\x81\x81\x01\x88\x19\x18\x18\x18\x00\x13\x13\x13\x93\x18\x18\x18\x18\x00\x00\x10\x9c\x02\x0d\x82\x96\x9a\x8b\x00\x00\x00\x00IEND\xaeB`\x82"
)


def png_file(name: str) -> ContentFile:
    return ContentFile(SMALL_PNG, name=name)


def file_from_static(rel_path: str, name: str | None = None) -> ContentFile:
    """Try to read a file from app static; fallback to tiny PNG if missing.

    rel_path is relative to app/static/app, e.g., 'bluediamondservicecenter/home/image1.jpg'.
    """
    # Typical BASE_DIR is '<repo>/core'; app static lives at '<repo>/core/app/static/app'
    base = Path(settings.BASE_DIR) / 'app' / 'static' / 'app'
    fpath = base / rel_path
    try:
        data = fpath.read_bytes()
        return ContentFile(data, name=name or fpath.name)
    except Exception:
        return png_file(name or 'placeholder.png')


LONG_SERVICE_HTML = (
    "<h3>Overview</h3>"
    "<p>Our certified technicians diagnose and resolve issues with meticulous care. We use genuine parts and follow manufacturer guidelines to ensure lasting performance.</p>"
    "<h3>What we include</h3>"
    "<ul>"
    "<li>Comprehensive inspection and safety checks</li>"
    "<li>Cleaning, lubrication, and calibration where applicable</li>"
    "<li>Parts replacement with warranty-backed components</li>"
    "<li>Final testing and customer guidance</li>"
    "</ul>"
    "<p>Schedule a visit and experience hassle-free service backed by years of expertise.</p>"
)

LONG_BLOG_HTML = (
    "<p>Appliance care isn’t just about fixing what’s broken—it’s about preventing problems before they occur. In this guide, we’ll walk through practical, field-tested tips used by our technicians.</p>"
    "<h3>Key practices</h3>"
    "<ol>"
    "<li>Follow a seasonal maintenance checklist tailored to your appliance.</li>"
    "<li>Use surge protection and proper ventilation to extend component life.</li>"
    "<li>Clean filters, coils, and seals regularly to maintain efficiency.</li>"
    "</ol>"
    "<h3>When to call a pro</h3>"
    "<p>If you notice burning smells, tripped breakers, or unusual noises, stop using the unit and book a professional inspection. Safety first.</p>"
)


class Command(BaseCommand):
    help = "Seeds the database with demo content for local/testing environments. Idempotent."

    def add_arguments(self, parser):
        parser.add_argument(
            "--min",
            type=int,
            default=20,
            help="Ensure at least this many rows exist for key models (services, courses, gallery, brands, testimonials, FAQs, blogs).",
        )

    def handle(self, *args, **options):
        self.min_count = max(1, int(options.get("min") or 20))
        self.stdout.write(self.style.WARNING(f"Seeding demo data (min per model: {self.min_count})..."))
        self.seed_company_and_home()
        self.seed_catalog()
        self.seed_engagement()
        self.seed_pages()
        self.seed_blog_and_videos()
        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))

    def seed_company_and_home(self):
        if not CompanyDetails.objects.exists():
            company = CompanyDetails(
                company_name="Blue Diamond Service Center",
                address="Kathmandu, Nepal",
                email="info@bluediamond.test",
                phone_number="+977-9800000000",
                map_location="https://www.google.com/maps?q=Kathmandu",
                facebook_url="https://facebook.com/",
                instagram_url="https://instagram.com/",
                description="Professional appliance repair and training services.",
            )
            company.logo.save("logo.png", file_from_static("bluediamondservicecenter/logo.png", "logo.png"), save=True)
            self.stdout.write("- CompanyDetails created")

        if not homesection.objects.exists():
            h = homesection(
                subtitle1="Welcome to Blue Diamond Service Center",
                subcontent1="We provide expert repair services for AC, refrigerators, washing machines, and more.",
                subtitle2="Professional Appliance Services You Can Trust",
                subcontent2="Fast response, genuine parts, and trained technicians.",
                subtitle3="Why Choose Us",
                subcontent3="Experienced team, reliable service, and customer-first approach.",
            )
            h.picture1.save("home.jpg", file_from_static("bluediamondservicecenter/home/image1.jpg", "home.jpg"), save=True)
            self.stdout.write("- homesection created")

        if Feature.objects.count() == 0:
            for i, title in enumerate(["Expert Technicians", "Genuine Parts", "Fast Support"], start=1):
                f = Feature(title=title, description="Quality you can trust.", sort_order=i, is_active=True)
                f.icon.save(f"feature_{i}.png", png_file(f"feature_{i}.png"), save=True)
            self.stdout.write("- Features created")

        if Carousel.objects.count() == 0:
            slides = [
                "bluediamondservicecenter/banner/slide1.jpg",
                "bluediamondservicecenter/banner/slide2.jpg",
                "bluediamondservicecenter/banner/slide3.jpg",
            ]
            for i, rel in enumerate(slides, start=1):
                c = Carousel(title=f"Slide {i}", description="Reliable service and support.", is_active=True)
                c.image.save(f"carousel_{i}.jpg", file_from_static(rel, f"carousel_{i}.jpg"), save=True)
            self.stdout.write("- Carousels created")

        # Banners for pages
        banner_pages = ["/about/", "/gallery/", "/enquiry/", "/contact/", "/services/", "/blog/"]
        for path in banner_pages:
            if not Banner.objects.filter(page_path=path).exists():
                b = Banner(title=f"Banner for {path}", page_path=path, is_active=True)
                b.image.save(
                    f"banner_{path.strip('/').replace('-', '_') or 'home'}.jpg",
                    file_from_static("bluediamondservicecenter/banner/bg1.jpg", "banner.jpg"),
                    save=True,
                )
        self.stdout.write("- Banners ensured")

    def seed_catalog(self):
        # Brands - top up to min
        bcount = Brand.objects.count()
        base_brands = [
            ("Samsung", "bluediamondservicecenter/brands/samsung.png"),
            ("LG", "bluediamondservicecenter/brands/lg.png"),
            ("Whirlpool", "bluediamondservicecenter/brands/whirlpool.png"),
            ("Godrej", "bluediamondservicecenter/brands/godrej.png"),
            ("Panasonic", "bluediamondservicecenter/brands/panasonic.png"),
            ("Hitachi", "bluediamondservicecenter/brands/whirlpool.png"),
        ]
        i = 0
        while Brand.objects.count() < self.min_count:
            base_name, rel = base_brands[i % len(base_brands)]
            name = f"{base_name} {Brand.objects.count()+1}"
            br = Brand(name=name, is_active=True)
            br.logo.save(f"brand_{Brand.objects.count()+1}.png", file_from_static(rel, "brand.png"), save=True)
            i += 1
        if Brand.objects.count() != bcount:
            self.stdout.write(f"- Brands ensured: {Brand.objects.count()}")

        # Services - top up to min (unique names)
        scount = Services.objects.count()
        service_imgs = [
            "bluediamondservicecenter/services/ac-repair-and-service.jpg",
            "bluediamondservicecenter/services/fridge-repair-and-service.jpg",
            "bluediamondservicecenter/services/washing-machine-repair-and-service.jpg",
            "bluediamondservicecenter/services/geyser-repair-and-installation-service.jpg",
            "bluediamondservicecenter/services/chimney-repair-and-service.jpg",
        ]
        service_names = [
            "AC Repair",
            "Refrigerator Repair",
            "Washing Machine Repair",
            "Geyser Installation",
            "Chimney Repair",
        ]
        ii = 0
        while Services.objects.count() < self.min_count:
            idx = Services.objects.count() + 1
            name = service_names[ii % len(service_names)] + f" {idx}"
            s = Services(
                name=name,
                short_description="Comprehensive diagnosis, cleaning, and performance optimization.",
                description=LONG_SERVICE_HTML,
                is_active=True,
            )
            rel = service_imgs[ii % len(service_imgs)]
            s.feature_image.save(f"service_{idx}.jpg", file_from_static(rel, f"service_{idx}.jpg"), save=True)
            ii += 1
        if Services.objects.count() != scount:
            self.stdout.write(f"- Services ensured: {Services.objects.count()}")

        # Gallery images - top up to min (associate with first service if available)
        gcount = GalleryImage.objects.count()
        svc = Services.objects.first()
        gallery_pool = service_imgs + [
            "bluediamondservicecenter/home/image1.jpg",
            "bluediamondservicecenter/home/image3.jpg",
        ]
        gi = 0
        while GalleryImage.objects.count() < self.min_count:
            idx = GalleryImage.objects.count() + 1
            g = GalleryImage(title=f"Work {idx}", service=svc, is_active=True)
            rel = gallery_pool[gi % len(gallery_pool)]
            g.image.save(f"gallery_{idx}.jpg", file_from_static(rel, f"gallery_{idx}.jpg"), save=True)
            gi += 1
        if GalleryImage.objects.count() != gcount:
            self.stdout.write(f"- Gallery images ensured: {GalleryImage.objects.count()}")

        # Training Courses - top up to min
        ccount = TrainingCourse.objects.count()
        while TrainingCourse.objects.count() < self.min_count:
            idx = TrainingCourse.objects.count() + 1
            tc = TrainingCourse(
                title=f"Course {idx}",
                short_description="Hands-on modules, safety, and troubleshooting.",
                description=LONG_SERVICE_HTML,
                is_active=True,
            )
            # Reuse a service image for course card
            rel = service_imgs[idx % len(service_imgs)]
            tc.image.save(f"course_{idx}.jpg", file_from_static(rel, f"course_{idx}.jpg"), save=True)
        if TrainingCourse.objects.count() != ccount:
            self.stdout.write(f"- Training courses ensured: {TrainingCourse.objects.count()}")

    def seed_engagement(self):
        # Testimonials - top up to min
        tcount = Testimonial.objects.count()
        while Testimonial.objects.count() < self.min_count:
            idx = Testimonial.objects.count() + 1
            t = Testimonial(
                name=f"Customer {idx}",
                location="Kathmandu",
                rating=5 if idx % 3 != 0 else 4,
                message="Great service! On-time, transparent, and professional.",
                is_active=True,
            )
            # Optional photo for first few testimonials
            if idx <= 2:
                rel = f"bluediamondservicecenter/testi{idx}.jpg"
                t.photo.save(f"testi_{idx}.jpg", file_from_static(rel, f"testi_{idx}.jpg"), save=True)
            else:
                t.save()
        if Testimonial.objects.count() != tcount:
            self.stdout.write(f"- Testimonials ensured: {Testimonial.objects.count()}")

        # FAQs - top up to min
        fcount = FAQ.objects.count()
        cats = [FAQ.GENERAL, FAQ.SERVICES, FAQ.PRICING, FAQ.TRAINING]
        while FAQ.objects.count() < self.min_count:
            idx = FAQ.objects.count() + 1
            FAQ.objects.create(
                question=f"Demo question {idx}?",
                answer="<p>Demo answer content.</p>",
                category=cats[idx % len(cats)],
                is_active=True,
                sort_order=idx,
            )
        if FAQ.objects.count() != fcount:
            self.stdout.write(f"- FAQs ensured: {FAQ.objects.count()}")

    def seed_pages(self):
        if not AboutUsPage.objects.exists():
            AboutUsPage.objects.create(
                page_title="About Us",
                main_heading="About Blue Diamond",
                content="<p>We are a trusted service center with certified technicians.</p>",
                is_active=True,
            )
            self.stdout.write("- AboutUsPage created")

        if not PrivacyPolicy.objects.exists():
            PrivacyPolicy.objects.create(page_title="Privacy Policy", content="<p>Your privacy matters.</p>", is_active=True)
            self.stdout.write("- PrivacyPolicy created")

        if not TermsAndConditions.objects.exists():
            TermsAndConditions.objects.create(page_title="Terms and Conditions", content="<p>Service terms and user responsibilities.</p>", is_active=True)
            self.stdout.write("- TermsAndConditions created")

    def seed_blog_and_videos(self):
        # Blog posts - top up to min (unique titles)
        bcount = BlogPost.objects.count()
        # Seed a few canonical posts first if none exist
        if bcount == 0:
            canonical = [
                ("AC Maintenance Tips", "Keep your AC running efficiently with these tips.", "<p>Change filters, clean coils, schedule service.</p>"),
                ("Diagnose Refrigerator Issues", "Common fridge problems and fixes.", "<p>Check power, thermostat, condenser coils.</p>"),
                ("Washing Machine Care", "Extend your washer's life.", "<p>Balance loads, clean drum, avoid overload.</p>"),
            ]
            for i, (title, excerpt, html) in enumerate(canonical, start=1):
                bp = BlogPost(title=title, excerpt=excerpt, content=html, is_published=True, published_at=timezone.now())
                # Use banner/home images for covers
                cover_rel = "bluediamondservicecenter/banner/bg3.jpg" if i == 1 else "bluediamondservicecenter/home/image3.jpg"
                bp.cover_image.save(f"blog_{i}.jpg", file_from_static(cover_rel, f"blog_{i}.jpg"), save=True)
            bcount = BlogPost.objects.count()
        while BlogPost.objects.count() < self.min_count:
            idx = BlogPost.objects.count() + 1
            bp = BlogPost(
                title=f"Demo Blog Post {idx}",
                excerpt="This is a demo excerpt for the blog post.",
                content=LONG_BLOG_HTML,
                is_published=True,
                published_at=timezone.now(),
            )
            # Alternate covers
            rel = "bluediamondservicecenter/banner/bg1.jpg" if idx % 2 == 0 else "bluediamondservicecenter/banner/slide2.jpg"
            bp.cover_image.save(f"blog_{idx}.jpg", file_from_static(rel, f"blog_{idx}.jpg"), save=True)
        if BlogPost.objects.count() != bcount:
            self.stdout.write(f"- Blog posts ensured: {BlogPost.objects.count()}")

        # Videos - ensure a few embeds (not necessarily 20)
        if Video.objects.count() < 3:
            vids = [
                ("AC Service Walkthrough", "Full AC servicing steps.", "https://www.youtube.com/embed/dQw4w9WgXcQ"),
                ("Refrigerator Coil Cleaning", "Why and how to clean coils.", "https://www.youtube.com/embed/ysz5S6PUM-U"),
                ("Washer Drum Cleaning", "Quick guide to drum cleaning.", "https://www.youtube.com/embed/oHg5SJYRHA0"),
            ]
            for title, desc, url in vids[: 3 - Video.objects.count()]:
                Video.objects.create(title=title, description=desc, embed_url=url, is_active=True)
            self.stdout.write(f"- Videos ensured: {Video.objects.count()}")
