# Lead Site Duplication Workflow
## How to launch a new local lead site in a new city or service vertical

This workflow is designed for fast duplication. Once you have the template,
each new site should take 2–4 hours to set up from scratch.

---

## STEP 1 — Choose Your Target (15 min)

Before buying a domain, validate the opportunity:

1. Google the main search term: "[service] quotes [city] SC"
2. Check if a Google Map Pack (3 local listings) appears — that means local intent
3. Check if competitors are running Google Ads — means money is there
4. Check domain availability at namecheap.com or Squarespace

**Green lights to proceed:**
- Search has 100–1,000 local monthly searches (use Google Keyword Planner)
- Map pack exists but listings are thin / unoptimized
- No dominant local lead site already ranking

---

## STEP 2 — Infrastructure Setup (30 min)

### Domain
- Register at Squarespace Domains (keeps DNS management in one place)
- Format: `[city][service].com` or `[city]scservices.com`
- Example: `darlingtonscservices.com`, `florenceacquotes.com`

### GitHub Repo
- Create new public repo: `[city]-[service]-site`
- Enable GitHub Pages: Settings → Pages → Deploy from main branch
- Add CNAME file to repo root with your domain

### DNS (Squarespace → GitHub Pages)
- Delete Squarespace Default A records
- Add 4 GitHub A records:
  - @ → 185.199.108.153
  - @ → 185.199.109.153
  - @ → 185.199.110.153
  - @ → 185.199.111.153
- Add 1 CNAME record:
  - www → [yourusername].github.io
- Wait 15–60 min for propagation
- GitHub repo → Settings → Pages → Custom domain → enter domain → Save → Enforce HTTPS

---

## STEP 3 — Build the Site (1–2 hours)

### Files to copy from this template:
- styles.css (no changes needed unless rebranding)
- script.js (update FORMSPREE and MAILTO constants at top)
- favicon.svg
- robots.txt (update domain)
- sitemap.xml (update domain + pages)
- CNAME (update domain)
- privacy.html (update business name + contact info)
- terms.html (update business name + contact info)

### Files to customize per site:
- index.html — update: business name, city, phone, email, hero copy, schema JSON-LD
- services.html — keep mostly the same, update city references
- pricing.html — keep mostly the same, update city references
- service-area.html — update city list and ZIP codes for this market
- about.html — update city and service description
- contact.html — update city, phone, email

### Find & Replace checklist (do this on ALL files):
| Find | Replace With |
|------|-------------|
| Florence SC Services | [New Business Name] |
| Florence, South Carolina | [New City], South Carolina |
| Florence, SC | [New City], SC |
| florencescservices.com | [new-domain].com |
| dumpsters@florencescservices.com | [newemail]@[new-domain].com |
| (843) 938-0480 | [New Tracking Number] |
| +18439380480 | +1[NewNumber] |
| 29501 | [New ZIP] |

---

## STEP 4 — Lead Capture Setup (30 min)

### Formspree
- Go to formspree.io → New Form
- Name it "[City] [Service] Leads"
- Copy endpoint URL
- Paste into script.js: `const FORMSPREE = 'https://formspree.io/f/XXXXXXXX'`
- Formspree free plan: 50 submissions/month (upgrade to $10/mo for unlimited)

### CallRail Tracking Number
- Log into CallRail → Numbers → New Number
- Select local area code for the target city
- Set forwarding to your real business/cell number
- Name it "[City] [Service] Site"
- Copy number → update all HTML files

### Google Analytics
- analytics.google.com → Admin → Create Property
- Name: "[City] [Service] Site"
- Copy Measurement ID (G-XXXXXXXXXX)
- Add to every HTML page <head>:
  ```html
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
  ```

---

## STEP 5 — Google Presence (1–2 hours, then ongoing)

### Google Search Console
- search.google.com/search-console → Add Property
- Verify via TXT record (add to Squarespace DNS → Custom Records)
- Submit sitemap: [domain]/sitemap.xml
- Check for errors after 48 hours

### Google Business Profile
- business.google.com → Add Business
- Name: [Business Name]
- Category: Waste Management Service
- Service area business (no storefront)
- Phone: [CallRail tracking number]
- Website: [domain]
- Write description (use template from DIRECTORY-COPY.md)
- Verify via postcard or phone
- Add 5+ photos (even stock photos of dumpsters help)

---

## STEP 6 — Citations (2–3 hours, one time per site)

Submit to all directories in this order using the DIRECTORY-COPY.md template.
Name/Address/Phone must be IDENTICAL everywhere.

Priority order:
1. Google Business Profile (already done in Step 5)
2. Yelp
3. Bing Places
4. Apple Maps
5. Facebook Business Page
6. BBB
7. Angi / Thumbtack
8. Yellowpages, Nextdoor, Foursquare, Manta

---

## STEP 7 — Launch QA Checklist

Before calling it live, run through this:

- [ ] Site loads at custom domain with HTTPS padlock
- [ ] All navigation links work on desktop and mobile
- [ ] Quote form submits successfully (test with real submission)
- [ ] Formspree confirmation email received
- [ ] Phone number is correct and forwards to your phone
- [ ] Call the number — it rings through correctly
- [ ] Footer NAP matches exactly what's in directory listings
- [ ] Google Search Console property created + sitemap submitted
- [ ] Google Business Profile claimed and verified (or verification in progress)
- [ ] GA4 tracking firing (check Realtime report)

---

## TIMELINE EXPECTATIONS

| Milestone | Typical Timeframe |
|-----------|------------------|
| Site live with HTTPS | Day 1 |
| Google indexes homepage | 3–7 days |
| GBP verified | 1–2 weeks (postcard) |
| Appearing in map pack | 4–8 weeks |
| Page 1 organic rankings | 3–6 months |
| Consistent lead flow | 4–6 months |

---

## SCALING PLAYBOOK

Once the Florence dumpster site is generating leads:

1. **Add more cities** — darlington.html, hartsville.html already exist as templates
2. **Add more services** — duplicate the entire repo for HVAC, plumbing, etc.
   - New domain: `florencescservices.com` can host multiple services OR
   - Separate domains for SEO isolation: `florenceacquotes.com`, `florenceplumbingquotes.com`
3. **Sell leads** — once you have consistent lead volume, approach local contractors
   directly and charge per lead ($15–75 depending on service) or flat monthly fee
4. **Build a portfolio** — 5–10 sites across Florence County services = passive income
   from lead sales with minimal ongoing maintenance

---

## COST STRUCTURE PER SITE

| Item | Cost |
|------|------|
| Domain (Squarespace) | ~$20/yr |
| GitHub Pages hosting | Free |
| Formspree (50 leads/mo) | Free |
| Formspree unlimited | $10/mo |
| CallRail tracking number | ~$3/mo + $45/mo base |
| Google everything | Free |
| **Total minimum** | **~$20/yr + your time** |
| **Total with call tracking** | **~$600/yr** |
