# Page SEO Management Guide

## Overview
The Page SEO feature allows you to configure custom SEO settings for static pages in your website. This is different from the regular SEO metadata which is for dynamic content like services, blog posts, and training courses.

## Accessing Page SEO in Dashboard

Navigate to: **Dashboard → SEO Management → Page SEO**

## What is Page SEO?

Page SEO is used for static pages like:
- **Homepage** - Your website's main landing page
- **Contact** - Contact us page
- **Services List** - Page showing all services
- **Training List** - Page showing all training courses
- **Blog List** - Page showing all blog posts
- **Gallery** - Image gallery page

## Difference: Page SEO vs SEO Metadata

| Feature | Page SEO | SEO Metadata |
|---------|----------|--------------|
| **Purpose** | Static pages (homepage, contact, etc.) | Dynamic content (individual services, blogs, courses) |
| **Location** | Dashboard → SEO Management → Page SEO | Automatically created when adding services/blogs/courses |
| **Quantity** | One per static page (max 6 pages) | One per content item (unlimited) |
| **Fields** | All standard SEO fields + Active status | All standard SEO fields + og_type, schema_type |
| **Auto-generation** | No auto-generation | Auto-generates from content if fields empty |

## How to Use Page SEO

### Step 1: View Existing Page SEO
1. Go to **Dashboard → SEO Management → Page SEO**
2. You'll see a list of all configured page SEO settings
3. Missing pages will be highlighted at the top with "Add SEO" links

### Step 2: Add SEO for a Page
1. Click **"Add SEO"** link next to the missing page OR
2. Click the general **"Add SEO"** button at the top
3. Select the page from the dropdown (e.g., "Homepage")
4. Check the **"Active"** checkbox to enable it
5. Fill in the SEO fields:
   - **Basic SEO**: Meta title, description, keywords, canonical URL
   - **Open Graph**: OG title, description, image (for Facebook sharing)
   - **Twitter Card**: Twitter title, description, image
   - **Advanced**: Robots meta, custom meta tags, JSON-LD schema

### Step 3: Edit Existing Page SEO
1. Click the **edit icon** (pencil) next to the page in the list
2. Modify any SEO fields as needed
3. Click **"Update Page SEO"** to save changes

### Step 4: Delete Page SEO
1. Click the **delete icon** (trash) next to the page
2. Confirm deletion in the modal popup
3. The page will revert to using global SEO settings

## SEO Priority System

The system uses the following priority when determining what SEO to display:

1. **Page SEO** (if exists and is_active = True) ← Highest priority
2. **Global SEO Settings** (fallback for static pages)
3. **Auto-generated SEO** (from page content)

Example for Homepage:
- If you configure Homepage Page SEO → Uses your custom settings
- If no Page SEO exists → Uses Global SEO Settings
- Both empty → Auto-generates basic SEO from site info

## Best Practices

### 1. Configure Homepage First
The homepage is the most important page for SEO. Always configure:
- Compelling meta title with main keyword (50-60 characters)
- Detailed meta description (150-160 characters)
- High-quality Open Graph image (1200x630px recommended)
- JSON-LD schema for Organization or Website

### 2. Use Unique Content for Each Page
Don't copy the same meta title/description across pages. Each should be unique:
- **Homepage**: Focus on brand and main value proposition
- **Services List**: Emphasize service variety and expertise
- **Contact**: Include location keywords and "contact us" phrases
- **Blog List**: Highlight topics and expertise areas

### 3. Optimize for Social Sharing
Fill in Open Graph and Twitter Card fields for better sharing:
- **OG Image**: Use branded images with text overlay
- **OG Description**: More engaging than meta description (can be longer)
- **Twitter Card Type**: Choose "summary_large_image" for visual impact

### 4. Keep Active Status in Mind
- Set `is_active = True` only when SEO is fully configured
- Temporarily disable by unchecking "Active" (doesn't delete data)
- Useful for A/B testing different SEO configurations

### 5. Monitor Missing Pages
The Page SEO list shows which static pages don't have custom SEO yet. Prioritize:
1. Homepage (critical)
2. Services List (important for service discovery)
3. Contact (local SEO)
4. Blog List (content marketing)
5. Training List (if offering courses)
6. Gallery (if visuals are key to your business)

## Common Use Cases

### Use Case 1: New Website Launch
1. Configure Homepage Page SEO with brand messaging
2. Set up Contact page with local keywords
3. Add Services List with service category keywords
4. Leave blog/training lists for later (fewer visitors initially)

### Use Case 2: SEO Improvement Campaign
1. Review existing Page SEO settings
2. Update meta titles to include primary keywords
3. Rewrite descriptions to improve click-through rate
4. Add structured data (JSON-LD) for rich snippets

### Use Case 3: Seasonal Promotions
1. Temporarily edit Homepage Page SEO
2. Add promotional keywords to meta title
3. Update OG image with seasonal banner
4. Revert after promotion ends

### Use Case 4: Local SEO Focus
1. Edit Contact Page SEO
2. Add city/region names to meta title
3. Include "near me" variations in keywords
4. Add LocalBusiness schema in JSON-LD field

## Troubleshooting

### Issue: Page SEO not showing on website
**Solution**: Check that:
- `is_active` checkbox is checked
- You've saved the form
- Cache is cleared (if using caching)
- View page source to verify meta tags

### Issue: Global SEO overriding Page SEO
**Solution**: 
- Ensure Page SEO is marked as Active
- Check that the correct page is selected in the dropdown
- Verify no code errors in template

### Issue: Can't add SEO for a page
**Solution**:
- Check if Page SEO already exists (edit instead)
- Ensure you selected a page from dropdown
- Look for validation errors in form

### Issue: Changes not visible in Google
**Solution**:
- Google takes time to re-crawl (days to weeks)
- Request re-indexing in Google Search Console
- Check robots.txt isn't blocking the page
- Verify meta tags in view source

## Technical Notes

- **Model**: `PageSEO` inherits from `BaseSEOMixin`
- **Unique Constraint**: One PageSEO per page (enforced by database)
- **Template Location**: `dashboard/templates/dashboard/page_seo_*.html`
- **View Classes**: `PageSEOListView`, `PageSEOAddEditView`, `PageSEODeleteView`
- **URL Namespace**: `dashboard:page_seo_list`, `dashboard:page_seo_add`, etc.

## Related Features

- **Global SEO Settings**: Fallback defaults for all pages
- **SEO Metadata**: For individual services, blogs, courses
- **Auto-generation**: Automatic SEO when fields empty

## Support

For questions or issues:
1. Check this guide first
2. Review the SEO field tooltips in the form
3. Test with "View Source" in browser
4. Contact support if issues persist
