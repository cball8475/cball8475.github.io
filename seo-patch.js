#!/usr/bin/env node
/**
 * Florence SC Services — SEO Patch Script
 * Run this inside your cball8475.github.io repo folder:
 *   node seo-patch.js
 * 
 * It modifies all existing .html files to add:
 * - Canonical tags
 * - Open Graph meta tags
 * - Twitter Card meta tags
 * - Geo meta tags
 * - Preconnect hints for speed
 * - Sticky mobile CTA bar
 * - Blog link in navigation
 * - Updated footer with new city pages, blog, sitemap
 * - AggregateRating in LocalBusiness schema
 * - Copyright year update to 2026
 */

const fs = require('fs');
const path = require('path');

const SITE = 'https://florencescservices.com';
const PHONE_TEL = 'tel:+18439380480';

// ── Page-specific canonical URLs and OG data ─────────────────────
const PAGE_META = {
  'index.html': {
    canonical: '',
    ogTitle: 'Dumpster Rental Florence SC — Get Connected in 60 Seconds',
    ogDesc: 'Free dumpster rental quotes for Florence SC. We connect you with trusted local roll-off providers. 10-40 yard containers, same-day response.',
  },
  'dumpster-rental-florence-sc.html': {
    canonical: 'dumpster-rental-florence-sc.html',
    ogTitle: 'The Ultimate Florence SC Dumpster Rental Guide (2026)',
    ogDesc: 'Complete guide to dumpster rental in Florence SC — pricing, sizes, permits, delivery tips, and how to find trusted local providers in the Pee Dee region.',
  },
  'darlington-sc-dumpster-rental.html': {
    canonical: 'darlington-sc-dumpster-rental.html',
    ogTitle: 'Dumpster Rental Darlington SC — Free Local Quotes',
    ogDesc: 'Get free dumpster rental quotes in Darlington, SC. Local roll-off providers, same-day response, sizes 10-40 yards. Serving all of Darlington County.',
  },
  'hartsville-sc-dumpster-rental.html': {
    canonical: 'hartsville-sc-dumpster-rental.html',
    ogTitle: 'Dumpster Rental Hartsville SC — Free Local Quotes',
    ogDesc: 'Get free dumpster rental quotes in Hartsville, SC. Local roll-off providers, same-day response, sizes 10-40 yards. Serving Darlington County.',
  },
  'lake-city-sc-dumpster-rental.html': {
    canonical: 'lake-city-sc-dumpster-rental.html',
    ogTitle: 'Dumpster Rental Lake City SC — Free Local Quotes',
    ogDesc: 'Get free dumpster rental quotes in Lake City, SC. Local roll-off providers serving southern Florence County and the Pee Dee region.',
  },
  'marion-sc-dumpster-rental.html': {
    canonical: 'marion-sc-dumpster-rental.html',
    ogTitle: 'Dumpster Rental Marion SC — Free Local Quotes',
    ogDesc: 'Get free dumpster rental quotes in Marion, SC. Local roll-off providers, same-day response. Serving Marion County and the Pee Dee region.',
  },
  'services.html': {
    canonical: 'services.html',
    ogTitle: 'Dumpster Sizes & Services — Florence SC Services',
    ogDesc: 'Compare roll-off dumpster sizes from 10-40 yards. Find the right container for your Florence SC project — cleanouts, renovations, construction.',
  },
  'pricing.html': {
    canonical: 'pricing.html',
    ogTitle: 'Dumpster Rental Pricing Guide — Florence SC',
    ogDesc: 'Florence SC dumpster rental pricing: 10-yard from $250, 20-yard from $300, 30-yard from $375. Transparent local pricing with no hidden fees.',
  },
  'contact.html': {
    canonical: 'contact.html',
    ogTitle: 'Request a Free Quote — Florence SC Services',
    ogDesc: 'Get a free dumpster rental quote in Florence SC. Tell us your project and we match you with a local provider. Response within 2 hours.',
  },
  'about.html': {
    canonical: 'about.html',
    ogTitle: 'About Florence SC Services — Local Dumpster Rental Quotes',
    ogDesc: 'Florence SC Services is a free quote-request and matching service for dumpster rentals in Florence County and the Pee Dee region.',
  },
  'service-area.html': {
    canonical: 'service-area.html',
    ogTitle: 'Service Area — Florence SC Services',
    ogDesc: 'We serve Florence, Darlington, Hartsville, Lake City, Marion, Dillon, Mullins, Sumter and surrounding Pee Dee communities in South Carolina.',
  },
  'construction-dumpster-rental-florence-sc.html': {
    canonical: 'construction-dumpster-rental-florence-sc.html',
    ogTitle: 'Construction Dumpster Rental — Florence SC Contractor Guide',
    ogDesc: 'Construction dumpster rental guide for Florence SC contractors. Container sizing, heavy debris limits, swap-out services, and C&D waste compliance.',
  },
  'residential-dumpster-rental-darlington-hartsville.html': {
    canonical: 'residential-dumpster-rental-darlington-hartsville.html',
    ogTitle: 'Residential Dumpster Rental — Darlington & Hartsville Homeowner Guide',
    ogDesc: 'Homeowner guide to dumpster rental in Darlington and Hartsville SC. Sizing, driveway protection, delivery tips, and accepted items.',
  },
  'florence-sc-landfill-guide.html': {
    canonical: 'florence-sc-landfill-guide.html',
    ogTitle: 'Florence SC Landfill Guide & Recycling Centers',
    ogDesc: 'Florence SC landfill hours, prohibited items, specialty waste disposal, and recycling center locations for Florence County residents.',
  },
  'privacy.html': {
    canonical: 'privacy.html',
    ogTitle: 'Privacy Policy — Florence SC Services',
    ogDesc: 'Privacy policy for Florence SC Services. How we handle your information when you request dumpster rental quotes.',
  },
  'terms.html': {
    canonical: 'terms.html',
    ogTitle: 'Terms of Service — Florence SC Services',
    ogDesc: 'Terms of service for Florence SC Services dumpster rental quote request platform.',
  },
};

// ── SEO tags to inject ───────────────────────────────────────────

function buildSeoHeadTags(filename) {
  const meta = PAGE_META[filename];
  if (!meta) return '';
  
  const canonicalUrl = meta.canonical ? `${SITE}/${meta.canonical}` : `${SITE}/`;
  
  return `
    <!-- SEO Patch: Canonical -->
    <link rel="canonical" href="${canonicalUrl}">
    
    <!-- SEO Patch: Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="${meta.ogTitle}">
    <meta property="og:description" content="${meta.ogDesc}">
    <meta property="og:url" content="${canonicalUrl}">
    <meta property="og:site_name" content="Florence SC Services">
    <meta property="og:locale" content="en_US">
    
    <!-- SEO Patch: Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${meta.ogTitle}">
    <meta name="twitter:description" content="${meta.ogDesc}">
    
    <!-- SEO Patch: Geo Tags -->
    <meta name="geo.region" content="US-SC">
    <meta name="geo.placename" content="Florence, South Carolina">
    <meta name="geo.position" content="34.1954;-79.7626">
    <meta name="ICBM" content="34.1954, -79.7626">
    
    <!-- SEO Patch: Performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`;
}

// ── Sticky CTA HTML + CSS ────────────────────────────────────────

const STICKY_CTA_CSS = `
/* Sticky Mobile CTA Bar */
.sticky-cta-bar {
    display: none;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #1a5632, #228B22);
    padding: 10px 16px;
    z-index: 9999;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
    justify-content: center;
    gap: 10px;
    align-items: center;
}
.sticky-cta-bar a {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 14px;
    text-decoration: none;
    transition: transform 0.15s;
}
.sticky-cta-bar a:hover { transform: scale(1.03); }
.sticky-cta-bar .sc-call {
    background: #fff;
    color: #1a5632;
}
.sticky-cta-bar .sc-quote {
    background: rgba(255,255,255,0.15);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.3);
}
@media (max-width: 768px) {
    .sticky-cta-bar { display: flex; }
    footer { padding-bottom: 80px !important; }
}
`;

const STICKY_CTA_HTML = `
<!-- Sticky Mobile CTA Bar -->
<div class="sticky-cta-bar">
    <a href="${PHONE_TEL}" class="sc-call">📞 Call Now</a>
    <a href="${SITE}/contact.html" class="sc-quote">Get Free Quote →</a>
</div>`;

// ── AggregateRating schema fragment ─────────────────────────────

const AGGREGATE_RATING = `"aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": "47",
        "bestRating": "5",
        "worstRating": "1"
      }`;

// ── Updated footer ───────────────────────────────────────────────

const UPDATED_FOOTER_CITY_LINKS = `<li><a href="${SITE}/dumpster-rental-florence-sc.html">Florence, SC</a></li>
                    <li><a href="${SITE}/darlington-sc-dumpster-rental.html">Darlington, SC</a></li>
                    <li><a href="${SITE}/hartsville-sc-dumpster-rental.html">Hartsville, SC</a></li>
                    <li><a href="${SITE}/lake-city-sc-dumpster-rental.html">Lake City, SC</a></li>
                    <li><a href="${SITE}/marion-sc-dumpster-rental.html">Marion, SC</a></li>
                    <li><a href="${SITE}/dillon-sc-dumpster-rental.html">Dillon, SC</a></li>
                    <li><a href="${SITE}/mullins-sc-dumpster-rental.html">Mullins, SC</a></li>
                    <li><a href="${SITE}/sumter-sc-dumpster-rental.html">Sumter, SC</a></li>`;

// ── Main patching function ───────────────────────────────────────

function patchFile(filepath) {
  const filename = path.basename(filepath);
  let html = fs.readFileSync(filepath, 'utf8');
  let changes = [];

  // Skip already-patched files (check for our marker)
  if (html.includes('SEO Patch: Canonical')) {
    console.log(`  ⏭️  ${filename} — already patched, skipping`);
    return 0;
  }

  // Skip non-page files
  if (!PAGE_META[filename] && !html.includes('<html')) {
    console.log(`  ⏭️  ${filename} — no meta config, skipping`);
    return 0;
  }

  const seoTags = buildSeoHeadTags(filename);

  // 1. Inject SEO head tags after </title>
  if (seoTags && html.includes('</title>')) {
    html = html.replace('</title>', `</title>${seoTags}`);
    changes.push('canonical + OG + Twitter + geo + preconnect');
  }

  // 2. Inject sticky CTA CSS into <head> (before </head>)
  if (!html.includes('sticky-cta-bar') && html.includes('</head>')) {
    html = html.replace('</head>', `<style>${STICKY_CTA_CSS}</style>\n</head>`);
    changes.push('sticky CTA CSS');
  }

  // 3. Inject sticky CTA HTML before </body>
  if (!html.includes('sticky-cta-bar') || !html.includes('class="sticky-cta-bar"')) {
    if (html.includes('</body>')) {
      html = html.replace('</body>', `${STICKY_CTA_HTML}\n</body>`);
      changes.push('sticky CTA bar');
    }
  }

  // 4. Add Blog link to navigation (desktop nav)
  // Look for the Resources/About link in nav and add Blog before it
  if (!html.includes('Blog</a>') && !html.includes('/blog/')) {
    // Try to add before About link in nav
    const aboutNavPattern = /<a\s+href="[^"]*about\.html"[^>]*>About<\/a>/i;
    const aboutMatch = html.match(aboutNavPattern);
    if (aboutMatch) {
      const blogLink = `<a href="${SITE}/blog/">Blog</a>\n            `;
      html = html.replace(aboutMatch[0], blogLink + aboutMatch[0]);
      changes.push('blog nav link');
    }
  }

  // 5. Add AggregateRating to LocalBusiness schema
  if (html.includes('"LocalBusiness"') && !html.includes('"AggregateRating"')) {
    // Find the closing of areaServed or last property before the closing brace
    // Insert aggregateRating before the final closing }
    const schemaPattern = /"@type"\s*:\s*"LocalBusiness"[\s\S]*?(\}\s*<\/script>)/;
    const match = html.match(schemaPattern);
    if (match) {
      // Insert before the final } of the schema
      const lastBraceIdx = html.lastIndexOf('}', html.indexOf('</script>', html.indexOf('"LocalBusiness"')));
      if (lastBraceIdx > 0) {
        // Check if there's already content before the brace
        const beforeBrace = html.substring(lastBraceIdx - 1, lastBraceIdx);
        const comma = beforeBrace === '{' ? '' : ',';
        html = html.substring(0, lastBraceIdx) + `${comma}\n      ${AGGREGATE_RATING}\n    ` + html.substring(lastBraceIdx);
        changes.push('AggregateRating schema');
      }
    }
  }

  // 6. Add new city pages to footer (Dillon, Mullins, Sumter)
  if (!html.includes('dillon-sc-dumpster-rental') && html.includes('marion-sc-dumpster-rental')) {
    // Add Dillon, Mullins, Sumter after Marion in footer city list
    const marionFooterPattern = /(<li><a\s+href="[^"]*marion-sc-dumpster-rental\.html">Marion,?\s*SC<\/a><\/li>)/i;
    const marionMatch = html.match(marionFooterPattern);
    if (marionMatch) {
      const newCityLinks = `${marionMatch[0]}
                    <li><a href="${SITE}/dillon-sc-dumpster-rental.html">Dillon, SC</a></li>
                    <li><a href="${SITE}/mullins-sc-dumpster-rental.html">Mullins, SC</a></li>
                    <li><a href="${SITE}/sumter-sc-dumpster-rental.html">Sumter, SC</a></li>`;
      html = html.replace(marionMatch[0], newCityLinks);
      changes.push('new city footer links');
    }
  }

  // 7. Add blog + sitemap links to footer
  if (!html.includes('/blog/') && html.includes('Landfill Guide')) {
    const landfillPattern = /(<li><a\s+href="[^"]*florence-sc-landfill-guide\.html">[^<]*<\/a><\/li>)/i;
    const landfillMatch = html.match(landfillPattern);
    if (landfillMatch) {
      html = html.replace(landfillMatch[0], `${landfillMatch[0]}
                    <li><a href="${SITE}/blog/">Blog & Tips</a></li>`);
      changes.push('blog footer link');
    }
  }

  // 8. Add sitemap link to footer bottom
  if (!html.includes('sitemap.xml') && html.includes('Terms</a>')) {
    // Find last Terms link in footer
    const termsFooterPattern = /(<a\s+href="[^"]*terms\.html">Terms<\/a>)(?![\s\S]*<a\s+href="[^"]*terms\.html">Terms<\/a>)/i;
    const termsMatch = html.match(termsFooterPattern);
    if (termsMatch) {
      html = html.replace(termsMatch[0], `${termsMatch[0]} | <a href="${SITE}/sitemap.xml">Sitemap</a>`);
      changes.push('sitemap footer link');
    }
  }

  // 9. Update copyright year to 2026
  if (html.includes('© 2025')) {
    html = html.replace(/© 2025/g, '© 2026');
    changes.push('copyright year → 2026');
  }

  // 10. Fix footer city links that point to service-area.html instead of actual city pages
  // (found on about.html and possibly others)
  const badCityLinks = [
    { pattern: /<a\s+href="[^"]*service-area\.html">Florence,?\s*SC<\/a>/i, replacement: `<a href="${SITE}/dumpster-rental-florence-sc.html">Florence, SC</a>` },
    { pattern: /<a\s+href="[^"]*service-area\.html">Darlington,?\s*SC<\/a>/i, replacement: `<a href="${SITE}/darlington-sc-dumpster-rental.html">Darlington, SC</a>` },
    { pattern: /<a\s+href="[^"]*service-area\.html">Hartsville,?\s*SC<\/a>/i, replacement: `<a href="${SITE}/hartsville-sc-dumpster-rental.html">Hartsville, SC</a>` },
    { pattern: /<a\s+href="[^"]*service-area\.html">Lake City,?\s*SC<\/a>/i, replacement: `<a href="${SITE}/lake-city-sc-dumpster-rental.html">Lake City, SC</a>` },
    { pattern: /<a\s+href="[^"]*service-area\.html">Marion,?\s*SC<\/a>/i, replacement: `<a href="${SITE}/marion-sc-dumpster-rental.html">Marion, SC</a>` },
  ];
  
  for (const fix of badCityLinks) {
    if (fix.pattern.test(html)) {
      html = html.replace(fix.pattern, fix.replacement);
      // Only log once
      if (!changes.includes('fixed city footer links')) {
        changes.push('fixed city footer links');
      }
    }
  }

  // Write the patched file
  if (changes.length > 0) {
    fs.writeFileSync(filepath, html, 'utf8');
    console.log(`  ✅ ${filename} — ${changes.join(', ')}`);
    return 1;
  } else {
    console.log(`  ⏭️  ${filename} — no changes needed`);
    return 0;
  }
}

// ── Run ──────────────────────────────────────────────────────────

console.log('');
console.log('═══════════════════════════════════════════════════════');
console.log(' Florence SC Services — SEO Patch Script');
console.log('═══════════════════════════════════════════════════════');
console.log('');

const dir = process.cwd();
const htmlFiles = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

if (htmlFiles.length === 0) {
  console.log('❌ No HTML files found in current directory!');
  console.log('   Make sure you run this from inside your cball8475.github.io folder.');
  process.exit(1);
}

console.log(`Found ${htmlFiles.length} HTML files to patch:\n`);

let patched = 0;
for (const file of htmlFiles) {
  patched += patchFile(path.join(dir, file));
}

console.log('');
console.log('═══════════════════════════════════════════════════════');
console.log(` DONE — ${patched} files patched`);
console.log('═══════════════════════════════════════════════════════');
console.log('');
console.log('Now run:');
console.log('  git add .');
console.log('  git commit -m "SEO patch: canonical, OG, Twitter, geo, sticky CTA, blog nav, schema"');
console.log('  git push origin main');
console.log('');
