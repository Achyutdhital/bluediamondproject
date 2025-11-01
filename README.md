# Blue Diamond Service Center - Admin Dashboard

This repository contains a Django project with a public site (`app`) and an internal admin dashboard (`dashboard`) built with class-based views and custom templates.

## Quick start

1. Install dependencies

```powershell
pip install -r requirements.txt
```

2. Run migrations (first time only)

```powershell
python .\core\manage.py migrate
```

3. Create a superuser (first time only)

```powershell
python .\core\manage.py createsuperuser
```

4. Start the dev server

```powershell
python .\core\manage.py runserver
```

5. Open the dashboard

- Visit: http://127.0.0.1:8000/dashboard/
- Login: http://127.0.0.1:8000/dashboard/login/

## Dashboard routes

- Home: `/dashboard/` (stats + recent activity)
- Auth: `/dashboard/login/`, `/dashboard/logout/`, `/dashboard/change-password/`
- Services: `/dashboard/services/` (add/edit/delete)
- Training Courses: `/dashboard/training-courses/` (add/edit/delete)
- Brands: `/dashboard/brands/` (add/edit/delete)
- Testimonials: `/dashboard/testimonials/` (add/edit/delete)
- FAQs: `/dashboard/faqs/` (add/edit/delete)
- Gallery: `/dashboard/gallery/` (add/edit/delete)
- Features: `/dashboard/features/` (add/edit/delete)
- Carousel: `/dashboard/carousels/` (add/edit/delete)
- Banners: `/dashboard/banners/` (add/edit/delete)
- Company Details: `/dashboard/company-details/`
- Home Section: `/dashboard/home-section/`
- About Us: `/dashboard/about-us/`
- Privacy Policy: `/dashboard/privacy-policy/`
- Terms & Conditions: `/dashboard/terms-conditions/`
- SEO Metadata: `/dashboard/seo-metadata/` (add/edit/delete)
- Enquiries: `/dashboard/enquiries/` (filter by status/search, detail view, update status)
- Contacts: `/dashboard/contacts/` (detail view, delete)

## Notes

- Image uploads are stored under `core/media/`.
- Rich-text fields are powered by CKEditor; ensure static files are collected for production.
- The sidebar in `dashboard/templates/dashboard/base.html` links to the routes above.

## Troubleshooting

- If images are not visible, confirm `MEDIA_URL` and `MEDIA_ROOT` in `core/core/settings.py` and that dev server serves media (it does in DEBUG mode via core/core/urls.py).
- If logins fail, ensure you created a user with `createsuperuser` and that cookies are enabled.
